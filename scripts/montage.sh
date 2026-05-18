#!/usr/bin/env bash
# Склейка: заставка (аватар + имя) -> видео с вшитыми субтитрами.
#
# Требуется: ffmpeg, ffprobe.
#
# Использование:
#   ./montage.sh <video> <subs.srt> <avatar> "<Имя>" [output.mp4] [intro_seconds]
#
# Пример:
#   ./montage.sh talk.mp4 talk.srt me.png "Иван Петров" final.mp4 4

set -euo pipefail

INPUT="${1:?Нужен путь к видео}"
SRT="${2:?Нужен путь к .srt}"
AVATAR="${3:?Нужен путь к картинке-аватарке}"
NAME="${4:?Нужно имя для заставки}"
OUTPUT="${5:-output.mp4}"
INTRO_SEC="${6:-3}"

for f in "$INPUT" "$SRT" "$AVATAR"; do
  [[ -f "$f" ]] || { echo "Не найден файл: $f" >&2; exit 1; }
done
command -v ffmpeg  >/dev/null || { echo "Нужен ffmpeg в PATH"  >&2; exit 1; }
command -v ffprobe >/dev/null || { echo "Нужен ffprobe в PATH" >&2; exit 1; }

# Параметры исходного видео — чтобы заставка совпала по размеру/fps.
read W H FPS_NUM FPS_DEN < <(
  ffprobe -v error -select_streams v:0 \
    -show_entries stream=width,height,r_frame_rate \
    -of csv=p=0:s=' ' "$INPUT" |
  awk '{split($3,a,"/"); printf "%s %s %s %s\n", $1, $2, a[1], (a[2]==""?1:a[2])}'
)
FPS="${FPS_NUM}/${FPS_DEN}"

# Размер аватарки и шрифта от высоты кадра.
AV=$(( H / 3 ))
FONT_SIZE=$(( H / 14 ))

# Шрифт с кириллицей. Можно переопределить через MONTAGE_FONT=/path/to/font.ttf.
FONT="${MONTAGE_FONT:-}"
if [[ -z "$FONT" ]]; then
  for candidate in \
    /usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf \
    /System/Library/Fonts/Supplemental/Arial.ttf \
    /Library/Fonts/Arial.ttf \
    "C:/Windows/Fonts/arialbd.ttf"
  do
    [[ -f "$candidate" ]] && FONT="$candidate" && break
  done
fi
[[ -n "$FONT" && -f "$FONT" ]] || { echo "Шрифт не найден. Задай MONTAGE_FONT=/path/to/font.ttf" >&2; exit 1; }

# Экранирование для drawtext и для пути к шрифту/субтитрам в filtergraph.
escape_drawtext() { printf '%s' "$1" | sed -e "s/\\\\/\\\\\\\\/g" -e "s/:/\\\\:/g" -e "s/'/\\\\\\\\'/g"; }
escape_path()     { printf '%s' "$1" | sed -e "s/\\\\/\\\\\\\\/g" -e "s/:/\\\\:/g" -e "s/'/\\\\'/g"; }

NAME_ESC=$(escape_drawtext "$NAME")
FONT_ESC=$(escape_path "$FONT")
SRT_ESC=$(escape_path "$SRT")

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
INTRO="$TMP/intro.mp4"
MAIN="$TMP/main.mp4"

# 1) Заставка: чёрный фон + круглый аватар + имя под ним + тихий звук
#    (тихий звук нужен, чтобы concat-демуксер совпал по дорожкам с основным видео).
ffmpeg -y -hide_banner -loglevel error \
  -f lavfi -i "color=c=black:s=${W}x${H}:r=${FPS}:d=${INTRO_SEC}" \
  -loop 1 -t "${INTRO_SEC}" -i "$AVATAR" \
  -f lavfi -t "${INTRO_SEC}" -i "anullsrc=channel_layout=stereo:sample_rate=48000" \
  -filter_complex "
    [1:v]scale=${AV}:${AV}:force_original_aspect_ratio=increase,crop=${AV}:${AV},format=rgba,
         geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(lt(hypot(X-${AV}/2,Y-${AV}/2),${AV}/2),255,0)'[av];
    [0:v][av]overlay=(W-w)/2:(H-h)/2-${AV}/3,
       drawtext=fontfile='${FONT_ESC}':text='${NAME_ESC}':fontcolor=white:fontsize=${FONT_SIZE}:
              x=(w-text_w)/2:y=(h/2)+${AV}/3+20
  " \
  -map "[v]" -map 2:a \
  -c:v libx264 -pix_fmt yuv420p -r "$FPS" \
  -c:a aac -ar 48000 -ac 2 -b:a 128k \
  -shortest "$INTRO" 2>&1 || {
    # Если фильтр не назвал выход [v], повторяем без -map (последний выход в filter_complex).
    ffmpeg -y -hide_banner -loglevel error \
      -f lavfi -i "color=c=black:s=${W}x${H}:r=${FPS}:d=${INTRO_SEC}" \
      -loop 1 -t "${INTRO_SEC}" -i "$AVATAR" \
      -f lavfi -t "${INTRO_SEC}" -i "anullsrc=channel_layout=stereo:sample_rate=48000" \
      -filter_complex "
        [1:v]scale=${AV}:${AV}:force_original_aspect_ratio=increase,crop=${AV}:${AV},format=rgba,
             geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='if(lt(hypot(X-${AV}/2,Y-${AV}/2),${AV}/2),255,0)'[av];
        [0:v][av]overlay=(W-w)/2:(H-h)/2-${AV}/3,
           drawtext=fontfile='${FONT_ESC}':text='${NAME_ESC}':fontcolor=white:fontsize=${FONT_SIZE}:
                  x=(w-text_w)/2:y=(h/2)+${AV}/3+20[v]
      " \
      -map "[v]" -map 2:a \
      -c:v libx264 -pix_fmt yuv420p -r "$FPS" \
      -c:a aac -ar 48000 -ac 2 -b:a 128k \
      -shortest "$INTRO"
  }

# 2) Основное видео с вшитыми субтитрами.
ffmpeg -y -hide_banner -loglevel error -i "$INPUT" \
  -vf "subtitles='${SRT_ESC}':force_style='Fontname=DejaVu Sans,Fontsize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=0,MarginV=40'" \
  -c:v libx264 -pix_fmt yuv420p -r "$FPS" \
  -c:a aac -ar 48000 -ac 2 -b:a 128k \
  "$MAIN"

# 3) Склейка через concat-демуксер. Кодеки/параметры у обеих частей одинаковые,
#    поэтому -c copy безопасен.
LIST="$TMP/list.txt"
{
  echo "file '$INTRO'"
  echo "file '$MAIN'"
} > "$LIST"

ffmpeg -y -hide_banner -loglevel error -f concat -safe 0 -i "$LIST" -c copy "$OUTPUT"

echo "Готово: $OUTPUT"
