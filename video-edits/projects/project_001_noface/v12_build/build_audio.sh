#!/bin/bash
# v7 audio: voice + 19 varied SFX + sidechain-ducked music
set -e
cd "$(dirname "$0")"

SFX=/home/user/teamplaner2/video-edits/sfx
MUSIC=/home/user/teamplaner2/video-edits/projects/project_001_noface/sources/footage/../../v4_build
# Music location:
MUSIC_FILE=/home/user/teamplaner2/video-edits/music/aqualina_orange_hues_201s.mp3
[ -f "$MUSIC_FILE" ] || MUSIC_FILE=$(find /home/user/teamplaner2/video-edits -name "aqualina*" -type f | head -1)
echo "Music: $MUSIC_FILE"

# 1) Voice (already built as voice.wav)
[ -f voice.wav ] || ffmpeg -y -hide_banner -loglevel error \
  -i ../sources/narrator_audio_53.5s.ogg \
  -af "atempo=1.10,loudnorm=I=-14:TP=-1.5:LRA=11,volume=2dB" voice.wav

# 2) 19 SFX events — each at its own moment, each a different file
# Format: SFX|time_seconds|filename|volume
SFX_LIST=(
  # v12: ONLY whooshes on SHARP cut/text-reveal moments. 20 → 7 events.
  "0.10|vylet_1.mp3|0.70"                        # hook entrance whoosh
  "6.36|fireball_whoosh_05224.mp3|0.85"          # hard cut M1→M2 night market
  "17.59|whoosh_grainy_2.mp3|0.85"               # +ВСЁ ТВОЁ big accent
  "32.90|fireball_whoosh.mp3|1.00"               # 120 BAT BIG IMPACT
  "40.40|whoosh_grainy_3.mp3|0.90"               # ЭМОЦИЯ accent
  "42.60|fast_blow_whoosh.mp3|0.95"              # ВАШ ПАСПОРТ finale
  "46.30|dust_whooshes.mp3|0.85"                 # CTA question card
)
# Pure whoosh-on-sharp-moments. No pops, glitch, buildup.
# Min gap between SFX: 2.2s (no back-to-back stacking that caused "перегруз" feeling).

# Build SFX mix command
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

echo "Building SFX mix (19 events)..."
ffmpeg -y -hide_banner -loglevel error $INPUTS -filter_complex "$FILT" -map "[sfx_mix]" -t 48.62 sfx.wav

# 3) Music: 48.7s slice from offset 10s, fades in/out, low volume
ffmpeg -y -hide_banner -loglevel error -i "$MUSIC_FILE" -ss 10 -t 48.7 \
  -af "afade=t=in:st=0:d=1.5,afade=t=out:st=46.7:d=2,volume=0.10" music_raw.wav

# 4) Sidechain duck music under voice
ffmpeg -y -hide_banner -loglevel error -i music_raw.wav -i voice.wav -filter_complex \
  "[0:a][1:a]sidechaincompress=threshold=0.02:ratio=20:attack=5:release=300:makeup=1:level_sc=2[out]" \
  -map "[out]" music_ducked.wav

# 5) Master mix: voice + sfx + music
ffmpeg -y -hide_banner -loglevel error -i voice.wav -i sfx.wav -i music_ducked.wav -filter_complex \
  "[0:a]volume=1.0[v];[1:a]volume=1.05[s];[2:a]volume=0.6[m];\
   [v][s][m]amix=inputs=3:duration=first:weights=1.0 1.05 0.6:normalize=0,\
   alimiter=limit=0.95[out]" -map "[out]" audio_master.wav

ffprobe -v error -show_entries format=duration -of csv=p=0 audio_master.wav
echo "Audio master built."
