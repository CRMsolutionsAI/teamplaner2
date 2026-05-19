#!/bin/bash
# prep_photo.sh — prepare photo for video edits.
# Accepts HEIC / HEIF / PNG / JPG / JPEG inputs.
#
# Usage:
#   ./prep_photo.sh photo.HEIC                       → photo.png (decoded, no bg removal)
#   ./prep_photo.sh photo.HEIC --transparent         → photo.png (background removed, RGBA)
#   ./prep_photo.sh photo.PNG --transparent          → photo.png (PNG → rembg cutout)
#   ./prep_photo.sh photo.jpg --transparent --output-dir sources/photos/
#   ./prep_photo.sh dir/*.HEIC dir/*.jpg -t -o cutouts/
#
# Tools:
#   - heif-convert (apt: libheif-examples) for HEIC/HEIF decode
#   - python3 + rembg (pip: rembg onnxruntime) for background removal
#
# AirDrop note: modern iOS Photos auto-converts to PNG/JPG on AirDrop to Mac,
# so HEIC is rarer now. PNG/JPG path is the common case.

set -euo pipefail

TRANSPARENT=false
OUTPUT_DIR=""
INPUTS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --transparent|-t) TRANSPARENT=true; shift ;;
    --output-dir|-o)  OUTPUT_DIR="$2"; shift 2 ;;
    *.heic|*.HEIC|*.heif|*.HEIF|*.png|*.PNG|*.jpg|*.JPG|*.jpeg|*.JPEG)
                      INPUTS+=("$1"); shift ;;
    *) echo "Skip unknown arg: $1" >&2; shift ;;
  esac
done

if [ ${#INPUTS[@]} -eq 0 ]; then
  echo "Usage: $0 <file.heic|png|jpg> [...] [--transparent] [--output-dir DIR]" >&2
  exit 1
fi

if $TRANSPARENT && ! python3 -c "import rembg" 2>/dev/null; then
  echo "ERR: rembg not installed. Install: pip install rembg onnxruntime" >&2
  exit 3
fi

mkdir -p "${OUTPUT_DIR:-.}"

for IN in "${INPUTS[@]}"; do
  if [ ! -f "$IN" ]; then
    echo "skip (not found): $IN" >&2
    continue
  fi

  base=$(basename "$IN" | sed 's/\.[^.]*$//')
  ext_lower=$(echo "${IN##*.}" | tr '[:upper:]' '[:lower:]')
  dir="${OUTPUT_DIR:-$(dirname "$IN")}"
  FINAL="$dir/${base}.png"

  echo "→ $IN"

  # Step 1: get a PNG copy (decode HEIC if needed; pass PNG through; convert JPG)
  if [[ "$ext_lower" == "heic" || "$ext_lower" == "heif" ]]; then
    if ! command -v heif-convert >/dev/null 2>&1; then
      echo "  ERR: heif-convert not found. Install libheif-examples." >&2
      continue
    fi
    TMP_PNG="$dir/${base}_decoded.png"
    heif-convert -q 95 "$IN" "$TMP_PNG" 2>&1 | tail -1
  elif [[ "$ext_lower" == "png" ]]; then
    TMP_PNG="$IN"  # use directly
  else
    # JPG → PNG via ffmpeg
    TMP_PNG="$dir/${base}_decoded.png"
    ffmpeg -y -hide_banner -loglevel error -i "$IN" "$TMP_PNG"
  fi

  # Step 2: background removal (if requested)
  if $TRANSPARENT; then
    python3 -c "
from rembg import remove
from PIL import Image
img = Image.open('$TMP_PNG')
out = remove(img)
out.save('$FINAL')
print('  bg removed → $FINAL')
"
    # Cleanup intermediate if it was a temp
    if [[ "$TMP_PNG" != "$IN" && "$TMP_PNG" != "$FINAL" ]]; then
      rm -f "$TMP_PNG"
    fi
  else
    if [[ "$TMP_PNG" != "$FINAL" ]]; then
      mv "$TMP_PNG" "$FINAL"
    fi
    echo "  saved → $FINAL"
  fi
done

echo ""
echo "✓ Done. ${#INPUTS[@]} file(s) processed."
