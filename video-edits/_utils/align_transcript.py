"""align_transcript.py — combine voice.wav silencedetect + transcript.txt
into a timestamped phrase map for accurate title placement.

Usage:
    python3 _utils/align_transcript.py path/to/voice.wav path/to/transcript.txt

Output (stdout):
    [0.66s] Встреча с тигром это не туристический аттракцион
    [6.08s] но это проверка твоей внутренней прошивки
    ...

Algorithm:
    1. Run silencedetect on voice.wav → phrase START boundaries
    2. Strip "Speaker N [HH:MM]:" prefixes from transcript
    3. Split transcript into sentences (.!?), keeping punctuation
    4. Distribute sentences across boundaries weighted by word count
       (predicted_start = cumulative_words / total_words × voice_duration)
    5. Snap each predicted_start to the nearest detected boundary
"""
import subprocess
import re
import sys
from pathlib import Path


def detect_phrase_starts(voice_wav: Path, noise: str = "-30dB", min_dur: float = 0.20):
    """Return list of voice-onset timestamps from silencedetect."""
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
    """Strip speaker prefixes, normalize whitespace, split by sentence punctuation."""
    txt = re.sub(r"Speaker\s+\d+\s*\[\d+:\d+\]:?\s*", "", txt, flags=re.IGNORECASE)
    txt = re.sub(r"Субтитры\s+создавал.*", "", txt, flags=re.IGNORECASE | re.DOTALL)
    txt = re.sub(r"\s+", " ", txt).strip()
    # Split by sentence boundaries — keep punctuation
    parts = re.split(r"(?<=[.!?])\s+(?=[А-ЯA-Z])", txt)
    return [p.strip() for p in parts if p.strip()]


def align(voice_wav: Path, transcript_text: str):
    starts = detect_phrase_starts(voice_wav)
    duration = voice_duration(voice_wav)
    sentences = split_transcript(transcript_text)

    if not sentences:
        return [], starts, duration

    word_counts = [len(s.split()) for s in sentences]
    total_words = sum(word_counts) or 1

    aligned = []
    cum_words = 0
    used_boundaries = set()
    for sent, wc in zip(sentences, word_counts):
        # Predicted position by word weight
        predicted = (cum_words / total_words) * duration
        # Find nearest unused boundary
        if starts:
            candidates = [(abs(b - predicted), b) for b in starts if b not in used_boundaries]
            if candidates:
                _, nearest = min(candidates)
                used_boundaries.add(nearest)
                aligned.append((nearest, sent))
            else:
                aligned.append((predicted, sent))
        else:
            aligned.append((predicted, sent))
        cum_words += wc

    aligned.sort(key=lambda x: x[0])
    return aligned, starts, duration


def main():
    if len(sys.argv) < 3:
        print("Usage: align_transcript.py <voice.wav> <transcript.txt>", file=sys.stderr)
        sys.exit(1)
    voice = Path(sys.argv[1])
    transcript_file = Path(sys.argv[2])
    if not voice.exists():
        print(f"ERR: voice file not found: {voice}", file=sys.stderr)
        sys.exit(1)
    if not transcript_file.exists():
        print(f"ERR: transcript file not found: {transcript_file}", file=sys.stderr)
        sys.exit(1)

    text = transcript_file.read_text(encoding="utf-8")
    aligned, starts, duration = align(voice, text)

    print(f"# Voice: {voice.name} ({duration:.2f}s) — {len(starts)} phrase boundaries detected")
    print(f"# Transcript: {len(aligned)} sentences aligned")
    print()
    for t, sent in aligned:
        # Truncate long sentences for readability in console output
        display = sent if len(sent) < 100 else sent[:97] + "..."
        print(f"[{t:6.2f}s] {display}")


if __name__ == "__main__":
    main()
