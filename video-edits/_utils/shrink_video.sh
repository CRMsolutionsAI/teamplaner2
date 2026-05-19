#!/bin/bash
# shrink_video.sh — re-encode video to fit chat upload limit (typically ≤30MB).
#
# Usage:
#   ./shrink_video.sh input.mp4                       → input_compact.mp4 (~25MB target)
#   ./shrink_video.sh input.MOV --target-mb 20        → 20MB target
#   ./shrink_video.sh input.mp4 --output out.mp4
#   ./shrink_video.sh *.mp4 --output-dir compact/
#
# Strategy:
#   1. Probe duration → calculate target bitrate = (target_mb * 8 * 1024) / duration_s [kbps]
#   2. Re-encode H.264 main profile with calculated bitrate
#   3. Audio AAC 96-128k (low priority — most chat losses are video)
#   4. +faststart for streaming compatibility
#
# Cloud env: ffmpeg is preinstalled.
# Mac: brew install ffmpeg

set -euo pipefail

TARGET_MB=25
OUTPUT=""
OUTPUT_DIR=""
INPUTS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --target-mb)   TARGET_MB="$2"; shift 2 ;;
    --output|-o)   OUTPUT="$2"; shift 2 ;;
    --output-dir)  OUTPUT_DIR="$2"; shift 2 ;;
    *.mp4|*.MP4|*.mov|*.MOV|*.m4v|*.M4V|*.mkv|*.MKV|*.webm|*.WEBM)
                   INPUTS+=("$1"); shift ;;
    *) echo "Skip unknown arg: $1" >&2; shift ;;
  esac
done

if [ ${#INPUTS[@]} -eq 0 ]; then
  echo "Usage: $0 <file.mp4> [...] [--target-mb 25] [--output out.mp4] [--output-dir DIR]" >&2
  exit 1
fi

[ -n "$OUTPUT_DIR" ] && mkdir -p "$OUTPUT_DIR"

for IN in "${INPUTS[@]}"; do
  if [ ! -f "$IN" ]; then
    echo "skip (not found): $IN" >&2
    continue
  fi

  # Resolve output path
  if [ -n "$OUTPUT" ] && [ ${#INPUTS[@]} -eq 1 ]; then
    OUT="$OUTPUT"
  else
    base=$(basename "$IN" | sed 's/\.[^.]*$//')
    dir="${OUTPUT_DIR:-$(dirname "$IN")}"
    OUT="$dir/${base}_compact.mp4"
  fi

  dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$IN")
  size_mb=$(du -m "$IN" | cut -f1)

  # Reserve ~10% for audio + container overhead → use 90% of budget for video
  audio_kbps=128
  video_kbps=$(awk -v mb=$TARGET_MB -v d=$dur -v a=$audio_kbps \
    'BEGIN{ printf "%d", (mb*1024*8*0.92)/d - a }')
  # Clamp to sane range
  if [ "$video_kbps" -lt 400 ]; then video_kbps=400; fi
  if [ "$video_kbps" -gt 8000 ]; then video_kbps=8000; fi

  printf "→ %s (%sMB, %.1fs) → target %sMB @ v%skbps a%skbps\n" \
    "$IN" "$size_mb" "$dur" "$TARGET_MB" "$video_kbps" "$audio_kbps"

  # Two-pass for accurate bitrate hitting
  PASS_LOG=$(mktemp -u /tmp/shrink_passXXXXXX)
  ffmpeg -y -hide_banner -loglevel error -i "$IN" \
    -c:v libx264 -profile:v main -pix_fmt yuv420p -preset medium \
    -b:v "${video_kbps}k" -maxrate "$((video_kbps * 13 / 10))k" -bufsize "$((video_kbps * 2))k" \
    -pass 1 -passlogfile "$PASS_LOG" -an -f mp4 /dev/null

  ffmpeg -y -hide_banner -loglevel error -i "$IN" \
    -c:v libx264 -profile:v main -pix_fmt yuv420p -preset medium \
    -b:v "${video_kbps}k" -maxrate "$((video_kbps * 13 / 10))k" -bufsize "$((video_kbps * 2))k" \
    -pass 2 -passlogfile "$PASS_LOG" \
    -c:a aac -b:a "${audio_kbps}k" -ar 44100 \
    -movflags +faststart \
    "$OUT"

  rm -f "${PASS_LOG}"-0.log "${PASS_LOG}"-0.log.mbtree

  out_size_mb=$(du -m "$OUT" | cut -f1)
  echo "  ✓ $OUT (${out_size_mb}MB)"
done

echo ""
echo "✓ Done. ${#INPUTS[@]} file(s) shrunk."
