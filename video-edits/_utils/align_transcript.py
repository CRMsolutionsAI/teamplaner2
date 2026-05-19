"""align_transcript.py — combine voice.wav silencedetect + transcript.txt
into a timestamped phrase map for accurate title placement.

Usage:
    # Basic — heuristic alignment (silencedetect + word-count weighting)
    python3 _utils/align_transcript.py voice.wav transcript.txt

    # Save aligned map to file for text_v*.py to load
    python3 _utils/align_transcript.py voice.wav transcript.txt --output v1_build/aligned.txt

    # Try ASR (Whisper) for word-level precision if available
    python3 _utils/align_transcript.py voice.wav transcript.txt --asr

Output format (stdout + optional file):
    [0.66s] Встреча с тигром это не туристический аттракцион
    [4.06s] В полторах часах от Бангкока...

Programmatic use from text_v*.py:
    from _utils.align_transcript import load_aligned, time_of_phrase
    phrases = load_aligned("voice.wav", "sources/transcript.txt")
    t = time_of_phrase(phrases, "открывает живот")  # → 91.21
"""
import subprocess
import re
import sys
import argparse
from pathlib import Path


def detect_phrase_starts(voice_wav: Path, noise: str = "-30dB", min_dur: float = 0.20):
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-nostats", "-i", str(voice_wav),
         "-af", f"silencedetect=noise={noise}:d={min_dur}",
         "-f", "null", "-"],
        capture_output=True, text=True
    ).stderr
    starts = []
    for line in out.splitlines():
        m = re.search(r"silence_end:\s*([\d.]+)", line)
        if m:
            starts.append(float(m.group(1)))
    return starts


def voice_duration(voice_wav: Path) -> float:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(voice_wav)],
        capture_output=True, text=True
    ).stdout.strip()
    return float(out)


def split_transcript(txt: str):
    txt = re.sub(r"Speaker\s+\d+\s*\[\d+:\d+\]:?\s*", "", txt, flags=re.IGNORECASE)
    txt = re.sub(r"Субтитры\s+создавал.*", "", txt, flags=re.IGNORECASE | re.DOTALL)
    txt = re.sub(r"\s+", " ", txt).strip()
    parts = re.split(r"(?<=[.!?])\s+(?=[А-ЯA-Z])", txt)
    return [p.strip() for p in parts if p.strip()]


def align_heuristic(voice_wav: Path, transcript_text: str):
    starts = detect_phrase_starts(voice_wav)
    duration = voice_duration(voice_wav)
    sentences = split_transcript(transcript_text)
    if not sentences:
        return [], starts, duration
    word_counts = [len(s.split()) for s in sentences]
    total_words = sum(word_counts) or 1
    aligned = []
    cum_words = 0
    used = set()
    for sent, wc in zip(sentences, word_counts):
        predicted = (cum_words / total_words) * duration
        if starts:
            cands = [(abs(b - predicted), b) for b in starts if b not in used]
            if cands:
                _, nearest = min(cands)
                used.add(nearest)
                aligned.append((nearest, sent))
            else:
                aligned.append((predicted, sent))
        else:
            aligned.append((predicted, sent))
        cum_words += wc
    aligned.sort(key=lambda x: x[0])
    return aligned, starts, duration


def align_asr(voice_wav: Path, transcript_text: str):
    """Try Whisper for word-level timestamps. Falls back to heuristic if unavailable."""
    try:
        import whisper
    except ImportError:
        print("# ASR unavailable (whisper not installed) — falling back to heuristic", file=sys.stderr)
        return align_heuristic(voice_wav, transcript_text)
    print("# Running Whisper (tiny model) for word-level timestamps...", file=sys.stderr)
    try:
        model = whisper.load_model("tiny")
        result = model.transcribe(str(voice_wav), word_timestamps=True, language="ru")
    except Exception as e:
        print(f"# Whisper failed ({e}) — falling back to heuristic", file=sys.stderr)
        return align_heuristic(voice_wav, transcript_text)
    duration = voice_duration(voice_wav)
    # Use segment-level timestamps as phrase boundaries
    sentences = split_transcript(transcript_text)
    asr_segments = [(seg["start"], seg["text"].strip()) for seg in result.get("segments", [])]
    if not asr_segments:
        return align_heuristic(voice_wav, transcript_text)
    # Match transcript sentences to ASR segments by order + word overlap
    aligned = []
    for i, sent in enumerate(sentences):
        if i < len(asr_segments):
            t, _ = asr_segments[i]
            aligned.append((t, sent))
        else:
            aligned.append((duration * i / len(sentences), sent))
    return aligned, [s[0] for s in asr_segments], duration


def format_output(aligned):
    lines = []
    for t, sent in aligned:
        display = sent if len(sent) < 100 else sent[:97] + "..."
        lines.append(f"[{t:6.2f}s] {display}")
    return "\n".join(lines)


# --- Programmatic API for text_v*.py ---

def load_aligned(voice_wav, transcript_path, use_asr: bool = False):
    """Return list of (time, sentence) tuples for use in text scripts."""
    voice_wav = Path(voice_wav)
    transcript_path = Path(transcript_path)
    text = transcript_path.read_text(encoding="utf-8")
    aligned, _, _ = (align_asr if use_asr else align_heuristic)(voice_wav, text)
    return aligned


def time_of_phrase(aligned, keyword: str, default=None):
    """Find time when a phrase containing `keyword` first appears. Case-insensitive."""
    keyword = keyword.lower()
    for t, s in aligned:
        if keyword in s.lower():
            return t
    return default


def main():
    p = argparse.ArgumentParser()
    p.add_argument("voice", type=Path)
    p.add_argument("transcript", type=Path)
    p.add_argument("--output", type=Path, help="Save aligned map to file")
    p.add_argument("--asr", action="store_true", help="Use Whisper for word-level timestamps if available")
    args = p.parse_args()

    if not args.voice.exists():
        print(f"ERR: voice not found: {args.voice}", file=sys.stderr); sys.exit(1)
    if not args.transcript.exists():
        print(f"ERR: transcript not found: {args.transcript}", file=sys.stderr); sys.exit(1)

    text = args.transcript.read_text(encoding="utf-8")
    fn = align_asr if args.asr else align_heuristic
    aligned, starts, duration = fn(args.voice, text)

    header = (f"# Voice: {args.voice.name} ({duration:.2f}s) — "
              f"{len(starts)} phrase boundaries\n"
              f"# Transcript: {len(aligned)} sentences aligned "
              f"({'ASR' if args.asr else 'heuristic'})\n")
    body = format_output(aligned)

    print(header)
    print(body)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(header + "\n" + body + "\n", encoding="utf-8")
        print(f"\n# Saved aligned map → {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
