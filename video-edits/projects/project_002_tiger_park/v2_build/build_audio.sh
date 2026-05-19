#!/bin/bash
set -e
cd "$(dirname "$0")"

SFX=/home/user/teamplaner2/video-edits/sfx
MUSIC=/home/user/teamplaner2/video-edits/music/deep_immersion/track_22_309s.mp3

DUR=108.21

# 6 whoosh SFX on sharp moments (re-timed for 108s)
SFX_LIST=(
  "0.10|vylet_1.mp3|0.70"                        # hook open
  "12.00|fireball_whoosh_05224.mp3|0.85"         # cut to "15 МИНУТ"
  "44.00|fast_blow_whoosh.mp3|1.00"              # BIG drop "5 ЭНЕРГИЙ" tier reveal
  "67.00|whoosh_grainy_2.mp3|0.90"               # BIG RULE "НЕ ЩЕКОЧИ СИЛУ"
  "91.00|fireball_whoosh.mp3|1.00"               # CLIMAX "открывает живот"
  "104.00|dust_whooshes.mp3|0.85"                # final CTA "МИР У ТВОИХ НОГ"
)

INPUTS=""
FILT=""
N=${#SFX_LIST[@]}
for i in "${!SFX_LIST[@]}"; do
  IFS='|' read -r T FN VOL <<< "${SFX_LIST[$i]}"
  INPUTS+=" -i $SFX/$FN"
  DELAY_MS=$(awk "BEGIN{printf \"%d\", $T*1000}")
  FILT+="[$i:a]volume=$VOL,adelay=${DELAY_MS}|${DELAY_MS}[s$i];"
done
MIX_INPUTS=""
for i in $(seq 0 $((N-1))); do MIX_INPUTS+="[s$i]"; done
FILT+="${MIX_INPUTS}amix=inputs=$N:duration=longest:normalize=0[sfx_mix]"

echo "Building SFX mix (6 whoosh)..."
ffmpeg -y -hide_banner -loglevel error $INPUTS -filter_complex "$FILT" -map "[sfx_mix]" -t $DUR sfx.wav

# Music
ffmpeg -y -hide_banner -loglevel error -i "$MUSIC" -ss 30 -t $(echo "$DUR + 0.2" | bc) \
  -af "afade=t=in:st=0:d=2.0,afade=t=out:st=$(echo "$DUR - 2.5" | bc):d=2.5,volume=0.10" music_raw.wav

# Sidechain duck
ffmpeg -y -hide_banner -loglevel error -i music_raw.wav -i voice.wav -filter_complex \
  "[0:a][1:a]sidechaincompress=threshold=0.02:ratio=18:attack=8:release=400:makeup=1:level_sc=2[out]" \
  -map "[out]" music_ducked.wav

# Master mix
ffmpeg -y -hide_banner -loglevel error -i voice.wav -i sfx.wav -i music_ducked.wav -filter_complex \
  "[0:a]volume=1.0[v];[1:a]volume=1.0[s];[2:a]volume=0.6[m];\
   [v][s][m]amix=inputs=3:duration=first:weights=1.0 1.0 0.6:normalize=0,\
   alimiter=limit=0.95[out]" -map "[out]" audio_master.wav

ffprobe -v error -show_entries format=duration -of csv=p=0 audio_master.wav
echo "Audio master built."
