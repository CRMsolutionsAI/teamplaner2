#!/bin/bash
# heic_to_png.sh — convert iPhone HEIC files to PNG with optional background removal.
#
# Usage:
#   ./heic_to_png.sh input.heic                    → input.png (full, no transparency)
#   ./heic_to_png.sh input.heic --transparent      → input.png (background removed, RGBA)
#   ./heic_to_png.sh dir/*.heic                    → batch
#   ./heic_to_png.sh dir/*.HEIC --transparent --output-dir out/
#
# Tools required:
#   - heif-convert  (apt: libheif-examples)  — for HEIC → PNG/JPG decode
#   - python3 + rembg  (pip: rembg onnxruntime)  — for background removal
#
# In cloud session both are already installed (verified 2026-05-19).
# On Mac: brew install libheif && pip install rembg onnxruntime

set -euo pipefail

TRANSPARENT=false
OUTPUT_DIR=""
INPUTS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --transparent|-t) TRANSPARENT=true; shift ;;
    --output-dir|-o)  OUTPUT_DIR="$2"; shift 2 ;;
    *.heic|*.HEIC|*.heif|*.HEIF) INPUTS+=("$1"); shift ;;
    *) echo "Skip unknown arg: $1" >&2; shift ;;
  esac
done

if [ ${#INPUTS[@]} -eq 0 ]; then
  echo "Usage: $0 <file.heic> [...] [--transparent] [--output-dir DIR]" >&2
  exit 1
fi

if ! command -v heif-convert >/dev/null 2>&1; then
  echo "ERR: heif-convert not found. Install via: apt install libheif-examples (Linux) / brew install libheif (Mac)" >&2
  exit 2
fi

if $TRANSPARENT && ! python3 -c "import rembg" 2>/dev/null; then
  echo "ERR: rembg not installed. Install via: pip install rembg onnxruntime" >&2
  exit 3
fi

mkdir -p "${OUTPUT_DIR:-.}"

for HEIC in "${INPUTS[@]}"; do
  base=$(basename "$HEIC" | sed 's/\.[hH][eE][iI][fF]\?$//')
  TMP_PNG="${OUTPUT_DIR:-$(dirname "$HEIC")}/${base}_full.png"
  FINAL_PNG="${OUTPUT_DIR:-$(dirname "$HEIC")}/${base}.png"

  echo "→ $HEIC"
  heif-convert -q 95 "$HEIC" "$TMP_PNG" 2>&1 | tail -1

  if $TRANSPARENT; then
    python3 -c "
from rembg import remove
from PIL import Image
img = Image.open('$TMP_PNG')
out = remove(img)
out.save('$FINAL_PNG')
print('  bg removed → $FINAL_PNG')
"
    rm -f "$TMP_PNG"
  else
    mv "$TMP_PNG" "$FINAL_PNG"
    echo "  saved → $FINAL_PNG"
  fi
done

echo ""
echo "✓ Done. ${#INPUTS[@]} file(s) processed."
