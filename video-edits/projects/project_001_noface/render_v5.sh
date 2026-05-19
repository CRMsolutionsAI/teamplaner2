#!/bin/bash
# render_v5.sh — Project 001 FINAL v6
# v6 changes: own covers for M1 hook, fixed IMG_0620 scale, single finale hero, louder voice
set -e

FFMPEG=/opt/homebrew/bin/ffmpeg
PRJ=/Users/natasa/teamplaner2/video-edits/projects/project_001_noface
SRC=$PRJ/sources
FTG=$SRC/footage
PXL=$FTG/pexels
PHO=$SRC/photos
MUSIC=/Users/natasa/teamplaner2/video-edits/music/all_good_now
SFX=/Users/natasa/teamplaner2/video-edits/sfx
FILT=$PRJ/filter_v5.txt
OUT=$PRJ/v_final.mp4

echo "=== Project 001 v6 render starting ==="

# Input layout (16 total):
# [0]  loop1       cover_green_dragon_clean.png  → M1 right + finale hero
# [1]  loop1       cover_black_mustache_clean.png → M1 left cover
# [2]              nm_28515504                   → M2 night market people (ambient)
# [3]              IMG_0620 lanterns             → M2 own footage (fixed scale)
# [4]              nm_28515508                   → M2 woman food (ambient)
# [5]              lw_34740034 leather           → M3 ambient craft
# [6]              IMG_0932                      → M3 own footage (split)
# [7]              ch_36164500 blacksmith        → M3 ambient
# [8]  stream_loop IMG_1110                      → M4 own footage
# [9]              IMG_0506                      → M4 own footage
# [10] loop1       IMG_7983.png                  → M4 product photo
# [11]             narrator audio
# [12]             music
# [13]             dust_swoosh SFX
# [14]             cartoon_bubble_pop
# [15]             film_title_transition

$FFMPEG -y \
  -loop 1             -i "$PHO/cover_green_dragon_clean.png" \
  -loop 1             -i "$PHO/cover_black_mustache_clean.png" \
                      -i "$PXL/nm_28515504_people_food_stand.mp4" \
                      -i "$FTG/IMG_0620_night_market_lanterns.mp4" \
                      -i "$PXL/nm_28515508_woman_food_stand.mp4" \
                      -i "$PXL/lw_34740034_leather_craft.mp4" \
                      -i "$FTG/IMG_0932.mp4" \
                      -i "$PXL/ch_36164500_blacksmith.mp4" \
  -stream_loop -1     -i "$FTG/IMG_1110.mp4" \
                      -i "$FTG/IMG_0506.mp4" \
  -loop 1             -i "$PHO/IMG_7983_passport_covers_finished.png" \
                      -i "$SRC/narrator_audio_53.5s.ogg" \
                      -i "$MUSIC/aqualina_orange_hues_201s.mp3" \
                      -i "$SFX/dust_swoosh.mp3" \
                      -i "$SFX/cartoon_bubble_pop.mp3" \
                      -i "$SFX/film_title_transition.mp3" \
  -/filter_complex "$FILT" \
  -map "[v_out]" \
  -map "[a_out]" \
  -c:v libx264 -crf 19 -preset medium \
  -c:a aac -b:a 192k \
  -pix_fmt yuv420p \
  -r 30 \
  -t 49.1 \
  "$OUT"

echo ""
echo "=== QC CHECK ==="
FFPROBE=/opt/homebrew/bin/ffprobe
$FFPROBE -v error -show_entries format=duration,size -of default=noprint_wrappers=1 "$OUT"
$FFPROBE -v error -select_streams v:0 \
  -show_entries stream=width,height,r_frame_rate,codec_name \
  -of default=noprint_wrappers=1 "$OUT"
$FFPROBE -v error -select_streams a:0 \
  -show_entries stream=codec_name,channels,bit_rate \
  -of default=noprint_wrappers=1 "$OUT"
$FFPROBE -v error -show_entries format_tags=title -of default=noprint_wrappers=1 "$OUT" 2>/dev/null || true
echo "=== DONE ==="
