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
  "0.10|vylet_1.mp3|0.55"                        # green dragon spring-in
  "2.05|dust_swoosh.mp3|0.65"                    # mustache slide-in (xfade)
  "3.90|film_title_transition.mp3|0.75"          # 2 covers reveal (xfade)
  "6.36|low_transition_6group.mp3|0.70"          # cut to night market
  "8.90|cartoon_bubble_pop.mp3|0.80"             # НОЧНОЙ РЫНОК text
  "12.10|puff_smoke_1.mp3|0.80"                  # ТЫ СОЗДАЁШЬ
  "13.49|puff_smoke_2.mp3|0.80"                  # СВОЮ СИСТЕМУ
  "15.12|whoosh_grainy_1.mp3|0.75"               # ЗНАЧКИ ЛЕНТА ЦВЕТ
  "17.40|sfx_aooo_29.mp3|0.85"                   # +ВСЁ ТВОЁ accent
  "18.78|whoosh_grainy_2.mp3|0.75"               # МАСТЕР
  "20.62|fast_blow_whoosh.mp3|0.75"              # ПАРУ МИНУТ
  "22.70|dust_whooshes.mp3|0.70"                 # ТАКТИЛЬНО НАДЁЖНО
  "25.42|unnamed_1.mp3|0.75"                     # СОЕДИНЯЕТ ДЕТАЛИ
  "28.50|film_humming_flight.mp3|0.70"           # NATALIA reveal
  "32.86|trailer_buildup.mp3|0.90"               # 120 BIG IMPACT — voice 33.01
  "36.45|sfx_04295.mp3|0.75"                     # = 161 ГРН
  "40.70|whoosh_grainy_3.mp3|0.80"               # ЭМОЦИЯ не чехол
  "42.94|trailer_spaceship.mp3|0.85"             # ВАШ ПАСПОРТ finale
  "46.43|vylet_2.mp3|0.75"                       # CTA "а во что одеты"
)

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
