#!/bin/bash
# render_v5.sh — Project 001 FINAL v5
# Applies all v2 feedback: atempo 1.09 + full subtitles + diagonal scatter + Pexels B-roll + cover PNGs
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

echo "=== Project 001 v5 render starting ==="
echo "Filter: $FILT"
echo "Output: $OUT"

$FFMPEG -y \
  -stream_loop -1     -i "$FTG/IMG_0468.mp4" \
                      -i "$PXL/nm_28515504_people_food_stand.mp4" \
                      -i "$FTG/IMG_0620_night_market_lanterns.mp4" \
                      -i "$PXL/nm_28515508_woman_food_stand.mp4" \
                      -i "$PXL/lw_34740034_leather_craft.mp4" \
                      -i "$FTG/IMG_0932.mp4" \
                      -i "$PXL/ch_36164500_blacksmith.mp4" \
  -stream_loop -1     -i "$FTG/IMG_1110.mp4" \
                      -i "$PXL/pp_7010563_passport_hand.mp4" \
                      -i "$PXL/sv_36861553_street_vendor_lights.mp4" \
  -loop 1             -i "$PHO/IMG_7983_passport_covers_finished.png" \
  -loop 1             -i "$PHO/cover_black_mustache.png" \
  -loop 1             -i "$PHO/cover_green_dragon.png" \
                      -i "$SRC/narrator_audio_53.5s.ogg" \
                      -i "$MUSIC/aqualina_orange_hues_201s.mp3" \
                      -i "$SFX/dust_swoosh.mp3" \
                      -i "$SFX/cartoon_bubble_pop.mp3" \
                      -i "$SFX/film_title_transition.mp3" \
  -filter_complex_script "$FILT" \
  -map "[v_out]" \
  -map "[a_out]" \
  -c:v libx264 -crf 19 -preset medium \
  -c:a aac -b:a 192k \
  -pix_fmt yuv420p \
  -r 30 \
  -t 49.1 \
  "$OUT"

echo ""
echo "=== DONE ==="
/opt/homebrew/bin/ffprobe -v error \
  -show_entries format=duration,size -of default=noprint_wrappers=1 "$OUT"
