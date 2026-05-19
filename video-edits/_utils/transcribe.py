"""transcribe.py — local-model Whisper transcription for cloud sessions.

Cloud egress blocks openai/HuggingFace model CDNs (verified 403). This script
loads Whisper from a model file committed to the repo (one-time push from Mac).

Setup (on Mac, once):
    pip install openai-whisper
    python3 -c "import whisper; whisper.load_model('tiny')"
    cp ~/.cache/whisper/tiny.pt video-edits/_utils/whisper-tiny.pt
    git add video-edits/_utils/whisper-tiny.pt && git push

Usage (in cloud):
    python3 _utils/transcribe.py sources/narrator_audio.ogg
    → sources/transcript.txt (plain text)
    → sources/transcript_with_timestamps.txt (segmented)

Programmatic:
    from _utils.transcribe import transcribe
    text, segments = transcribe("audio.ogg")
"""
import os
import sys
import argparse
from pathlib import Path


MODEL_DIR = Path(__file__).resolve().parent
# Priority: larger models first (better accuracy). Found-first wins.
MODEL_NAMES = [
    ("whisper-large-v3.pt", "large-v3"),
    ("whisper-large-v2.pt", "large-v2"),
    ("whisper-large.pt",    "large"),
    ("whisper-medium.pt",   "medium"),
    ("whisper-small.pt",    "small"),
    ("whisper-base.pt",     "base"),
    ("base.pt",             "base"),
    ("whisper-tiny.pt",     "tiny"),
    ("tiny.pt",             "tiny"),
]


def find_model() -> tuple[Path, str]:
    """Find local Whisper model in _utils/. Return (path, model_size).

    Searches in priority order (largest → smallest) so if user pushes 'base'
    it gets preferred over 'tiny'.
    """
    for name, size in MODEL_NAMES:
        path = MODEL_DIR / name
        if path.exists() and not path.is_symlink():
            return path, size
    return None, None


def transcribe(audio_path, language: str = "ru"):
    """Transcribe audio. Returns (full_text, segments_list).

    segments_list = [{'start': float, 'end': float, 'text': str}, ...]
    """
    try:
        import whisper
    except ImportError:
        raise RuntimeError(
            "whisper package not installed. Run: pip install openai-whisper"
        )

    model_path, model_size = find_model()
    if model_path is None:
        raise RuntimeError(
            f"No Whisper model found in {MODEL_DIR}.\n"
            f"On Mac, run:\n"
            f"  python3 -c \"import whisper; whisper.load_model('tiny')\"\n"
            f"  cp ~/.cache/whisper/tiny.pt {MODEL_DIR}/whisper-tiny.pt\n"
            f"  git add {MODEL_DIR.relative_to(Path.cwd())}/whisper-tiny.pt && git push"
        )

    # whisper.load_model checks download_root first; place model symlink-style
    # via download_root pointing at MODEL_DIR. Whisper expects file named e.g. "tiny.pt"
    download_root = MODEL_DIR
    # Ensure canonical name exists for whisper to find
    canonical = MODEL_DIR / f"{model_size}.pt"
    if not canonical.exists():
        canonical.symlink_to(model_path.name)

    print(f"# Loading Whisper {model_size} from {model_path}", file=sys.stderr)
    model = whisper.load_model(model_size, download_root=str(download_root))

    print(f"# Transcribing {audio_path} (lang={language})...", file=sys.stderr)
    result = model.transcribe(
        str(audio_path),
        language=language,
        word_timestamps=False,
        verbose=False,
    )
    return result["text"].strip(), result.get("segments", [])


def main():
    p = argparse.ArgumentParser()
    p.add_argument("audio", type=Path)
    p.add_argument("--language", default="ru")
    p.add_argument("--output", type=Path,
                   help="Plain text output path")
    p.add_argument("--with-timestamps", type=Path,
                   help="Timestamped version path")
    p.add_argument("--save-to-project", type=str, metavar="PROJ_NAME",
                   help="Save transcript directly to projects/<PROJ_NAME>/sources/transcript.txt "
                        "(auto-resolves repo path). Overrides --output.")
    args = p.parse_args()

    if not args.audio.exists():
        print(f"ERR: audio not found: {args.audio}", file=sys.stderr)
        sys.exit(1)

    try:
        text, segments = transcribe(args.audio, args.language)
    except RuntimeError as e:
        print(f"ERR: {e}", file=sys.stderr)
        sys.exit(2)

    # Resolve outputs
    if args.save_to_project:
        # Find projects/ root relative to this script
        projects_root = Path(__file__).resolve().parents[1] / "projects"
        proj_dir = projects_root / args.save_to_project
        if not proj_dir.is_dir():
            print(f"ERR: project not found: {proj_dir}", file=sys.stderr)
            sys.exit(3)
        out_plain = proj_dir / "sources" / "transcript.txt"
        out_ts = proj_dir / "sources" / "transcript_with_timestamps.txt"
        out_plain.parent.mkdir(parents=True, exist_ok=True)
    else:
        out_plain = args.output or args.audio.parent / "transcript.txt"
        out_ts = args.with_timestamps or args.audio.parent / "transcript_with_timestamps.txt"

    out_plain.write_text(text + "\n", encoding="utf-8")
    print(f"✓ {out_plain}  ({len(text)} chars)", file=sys.stderr)

    with out_ts.open("w", encoding="utf-8") as f:
        for seg in segments:
            f.write(f"[{seg['start']:6.2f} → {seg['end']:6.2f}] {seg['text'].strip()}\n")
    print(f"✓ {out_ts}  ({len(segments)} segments)", file=sys.stderr)

    # Print full plain text to stdout for downstream piping
    print(text)


if __name__ == "__main__":
    main()
