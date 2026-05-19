#!/bin/bash
set -e
cd "$(dirname "$0")"

# Reuse v2 voice (same processing — atempo 1.20, no silenceremove)
if [ ! -f voice.wav ]; then
  ffmpeg -y -hide_banner -loglevel error -i ../sources/narrator_audio.ogg \
    -af "atempo=1.20,loudnorm=I=-14:TP=-1.5:LRA=11,volume=1.5dB" voice.wav
fi

SFX=/home/user/teamplaner2/video-edits/sfx
MUSIC=/home/user/teamplaner2/video-edits/music/deep_immersion/track_22_309s.mp3
DUR=108.21

# 6 whoosh on sharp moments, re-timed to v3 storyboard
SFX_LIST=(
  "0.10|vylet_1.mp3|0.70"                        # hook open
  "12.00|fireball_whoosh_05224.mp3|0.85"         # cut to "15 МИНУТ" card
  "44.00|fast_blow_whoosh.mp3|1.00"              # 5 ЭНЕРГИЙ tier reveal
  "66.00|whoosh_grainy_2.mp3|0.90"               # BIG RULE "НЕ ЩЕКОЧИ СИЛУ"
  "83.00|fireball_whoosh.mp3|1.00"               # belly photo impact
  "101.00|dust_whooshes.mp3|0.85"                # final CTA
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

ffmpeg -y -hide_banner -loglevel error $INPUTS -filter_complex "$FILT" -map "[sfx_mix]" -t $DUR sfx.wav
# Music with dynamics: base 0.10, swell to 0.16 around 66s (BIG RULE) and 87s (climax)
ffmpeg -y -hide_banner -loglevel error -i "$MUSIC" -ss 30 -t $(echo "$DUR + 0.2" | bc) \
  -af "afade=t=in:st=0:d=2.0,afade=t=out:st=$(echo "$DUR - 2.5" | bc):d=2.5,\
volume='0.10 + 0.06*(between(t,64,69) + between(t,85,90))':eval=frame" music_raw.wav
ffmpeg -y -hide_banner -loglevel error -i music_raw.wav -i voice.wav -filter_complex \
  "[0:a][1:a]sidechaincompress=threshold=0.02:ratio=18:attack=8:release=400:makeup=1:level_sc=2[out]" \
  -map "[out]" music_ducked.wav
ffmpeg -y -hide_banner -loglevel error -i voice.wav -i sfx.wav -i music_ducked.wav -filter_complex \
  "[0:a]volume=1.0[v];[1:a]volume=1.0[s];[2:a]volume=0.6[m];\
   [v][s][m]amix=inputs=3:duration=first:weights=1.0 1.0 0.6:normalize=0,\
   alimiter=limit=0.95[out]" -map "[out]" audio_master.wav
echo "Audio master built."
