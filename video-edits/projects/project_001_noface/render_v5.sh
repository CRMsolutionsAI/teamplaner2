#!/bin/bash
# render_v5.sh — Project 001 FINAL v6
# v3 criticals: narrator audible, NO product stock, only own footage for product shots
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

echo "=== Project 001 v6 (v3 fixes) render starting ==="

# Input layout (18 total):
# [0]  stream_loop IMG_0468       M1 hook
# [1]  nm_28515504                M2 night market ambient
# [2]  IMG_0620 lanterns          M2 own footage
# [3]  nm_28515508                M2 ambient
# [4]  lw_34740034 leather        M3 ambient craft
# [5]  IMG_0932                   M3 own footage
# [6]  ch_36164500 blacksmith     M3 ambient
# [7]  stream_loop IMG_1110       M4 own footage
# [8]  IMG_0506                   M4 own footage
# [9]  loop IMG_7983.png          M4+finale own product photo
# [10] loop cover_black_mustache  finale own product
# [11] loop cover_green_dragon    finale own product
# [12] narrator audio
# [13] music
# [14] dust_swoosh SFX
# [15] cartoon_bubble_pop
# [16] film_title_transition

$FFMPEG -y \
  -stream_loop -1     -i "$FTG/IMG_0468.mp4" \
                      -i "$PXL/nm_28515504_people_food_stand.mp4" \
                      -i "$FTG/IMG_0620_night_market_lanterns.mp4" \
                      -i "$PXL/nm_28515508_woman_food_stand.mp4" \
                      -i "$PXL/lw_34740034_leather_craft.mp4" \
                      -i "$FTG/IMG_0932.mp4" \
                      -i "$PXL/ch_36164500_blacksmith.mp4" \
  -stream_loop -1     -i "$FTG/IMG_1110.mp4" \
                      -i "$FTG/IMG_0506.mp4" \
  -loop 1             -i "$PHO/IMG_7983_passport_covers_finished.png" \
  -loop 1             -i "$PHO/cover_black_mustache.png" \
  -loop 1             -i "$PHO/cover_green_dragon.png" \
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
echo "=== DONE ==="
