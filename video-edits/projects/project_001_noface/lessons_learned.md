# Project_001 — Lessons Learned

**Финальная версия:** `v_final.mp4` (49.1с, vertical 1080x1920)
**Дата v5:** 2026-05-19 (v2-правки применены)

## ✅ Что получилось лучше всего

1. **Black canvas + frame-in-frame архитектура** — сохранена. Видео-окна на чёрном фоне работают как design composition. Новые Pexels-клипы вписались без швов.

2. **Полные субтитры через Whisper STT** — faster-whisper дал точные тайминги на уровне слов. 24 субтитрных строки с fade-in/fade-out, нижняя safe zone y=1728. Ключевые фразы (сейф, мини-перформанс, надёжность, 120 бат, история) — оранжевым `0xFF5722`.

3. **Diagonal scatter text reveal** — 3 слова появляются по диагонали с шагом 0.3с (x=60→350→620, y=190→340→490). Применено в M1 (ОБРАТИ/ВНИМАНИЕ/НА), M2 (НОЧНОЙ/РЫНОК/ТАИЛАНД), M3 (МАСТЕР/+МАГИЯ/НАДЁЖНОСТЬ). Паттерн работает — фразы «собираются» как layout.

4. **Pexels B-roll pipeline** — 7 новых клипов (night market ×3, leather workshop, blacksmith, passport hand, street vendor lights) органично встроены в монтаж. API → curl → filter_complex PTS-shift — надёжный workflow.

5. **Ускоренный темп (atempo=1.09)** — 53.5с → 49.1с, речь стала заметно динамичнее. Финальная длина = длине сжатого аудио.

6. **Cover PNG финальная карточка** — cover_black_mustache и cover_green_dragon скользят с боков (left slide + right slide) поверх IMG_7983 в финальной секции. colorkey убирает белый фон.

7. **Multi-tier finale** «ВАШ / ПАСПОРТ / — *ваша история*» сохранён — один из лучших closing-cards в библиотеке.

## 🎯 Конкретное усложнение для следующего ролика

**Word-level iOS highlighter** — в v5 хайлайт работает на УРОВНЕ СТРОКИ (вся строка оранжевая). Следующий шаг: добавить drawbox точно под СЛОВО внутри строки. Для этого нужны слова с точным `text_w` — либо pre-render через Pillow с измерением, либо Whisper word-timestamps + ручной drawbox с приближёнными координатами.

Конкретно: для слова «сейф» в центрированной строке «это «сейф» для моих документов,» нужно знать позицию слова в пикселях. Можно через `drawtext` с `textfile` + `fontmetrics`.

## 📋 Чек-лист контроля качества (v5)

- [x] Нет чёрных экранов (черный = design background)
- [x] Длина ролика = длине аудио (49.1с = atempo'd 53.5/1.09)
- [x] Иерархия громкости: narrator > sfx (0.22-0.35) > music (0.1)
- [x] Sidechain ducking музыки под голос
- [x] Весь текст в safe zone (subtitle y=1728, top text y≥190)
- [x] Frame-in-frame на черном фоне (без letterbox)
- [x] Color grade eq=contrast=1.12:saturation=1.08
- [x] Sign-off: «ВАШ / ПАСПОРТ / — ваша история» (multi-tier)
- [x] Бренд-цвет #FF5722 везде
- [x] Full subtitles 24 строки по всей длине

## 🔁 Новые техники (добавлены в v5)

| Техника | Применено |
|---|---|
| Whisper STT → word timestamps → drawtext subtitles | Все 24 строки |
| Diagonal scatter 3-word reveal (X+290px, Y+150px, Δt=0.3s) | M1, M2, M3 |
| Pexels API B-roll download → PTS-shift overlay | 7 клипов |
| atempo=1.09 speedup сохраняя sync с субтитрами | Нарратор |
| colorkey=white removal на PNG с продуктом | cover_black/green |
| PNG slide-in animation через overlay x=expr | Финальная карточка |

## 📝 Технические данные (v5)

- **Кодек:** H.264, CRF 19, preset medium, AAC 192k
- **Разрешение:** 1080x1920 @ 30fps
- **Длительность:** 49.1с
- **Размер:** ~29 МБ
- **Музыка:** `all_good_now/aqualina_orange_hues_201s.mp3`
- **SFX:** 7 точек (dust_swoosh ×5, cartoon_bubble_pop, film_title_transition)
- **Шрифты:** Roboto Condensed Bold (display) + Caveat (handwriting)
- **Color grade:** `eq=contrast=1.12:saturation=1.08:gamma_r=0.96:gamma_b=1.04`
- **B-roll Pexels IDs:** 28515504, 28515508, 30119040, 34740034, 36164500, 7010563, 36861553
- **Filter script:** `filter_v5.txt` (Python-generated via `gen_filter.py`)

## 🔴 КРИТИЧЕСКИЕ БАГИ v5 → ИСПРАВЛЕНЫ в v6

### Баг 1: Голос диктора пропал из микса
**Причина:** `[narrator]` был использован ДВАЖДЫ без `asplit`:
1. Как sidechain-ключ для sidechaincompress (`[mraw][narrator]sidechaincompress...`)
2. Как вход в amix (`[narrator][mducked]...amix`)

ffmpeg не может дать один поток двум потребителям — голос ушёл в ноль.

**Исправление:** `[12:a]atempo=1.09,loudnorm=...,asplit=2[narrator][narrator_sc]`
— `[narrator_sc]` → sidechain ключ (duck музыку)
— `[narrator]` → в финальный amix (первый план)

**Правило навсегда:** при sidechain ducking ВСЕГДА делать `asplit=2` на вокале до отправки в два места.

### Баг 2: Стоковые видео паспортов в продуктовой секции
`pp_7010563` (passport hand) и `sv_36861553` (street vendor) использовались в M4 — секции показа продукта.

**Исправление:** заменены на `IMG_0506.mp4` + `IMG_7983.png` (собственные файлы клиента).

## 🔴 КРИТИЧЕСКИЕ БАГИ v5/v6 → ИСПРАВЛЕНЫ в v6

### Баг 3: scale=ODD:H для горизонтального клипа → чёрная дыра
`scale=2667:1493` — нечётное значение ширины (2667) вызывало ошибку компоновки для IMG_0620 (1280×720).
**Исправление:** `scale=-2:1493,crop=840:1493` — `-2` автоматически округляет до чётного.
**Правило:** всегда использовать `-2` (не `-1`) для авто-ширины в ffmpeg.

### Баг 4: loudnorm + volume boost = True Peak клиппинг
`loudnorm=I=-16:TP=-1.5,volume=2.0` → peaks идут до +4.5 dBTP (клиппинг!).
**Исправление (для следующего раза):** снизить target внутри loudnorm:
`loudnorm=I=-22:TP=-7.5:LRA=11,volume=2.0` → после +6dB → I=-16, TP=-1.5 (без клиппинга).

### Баг 5: eof_action на PNG covers без trimmed-stream
loop1 PNG-клипы после trim=6.4s замерзают на последнем кадре (eof_action=repeat по умолчанию).
**Исправление:** `:eof_action=pass` на overlay → после конца стрима показывает base-слой, не frozen frame.

## ✅ V6 — Что изменилось (2026-05-19)

| Изменение | Что было | Что стало |
|---|---|---|
| M1 hook | IMG_0468 (стоковый vendor) | cover_black_mustache_clean + cover_green_dragon_clean (свои обложки) |
| IMG_0620 scale | `scale=2667:1493` (odd width → чёрная дыра) | `scale=-2:1493,crop=840:1493` (FIF, ровный) |
| Финал t=40-49s | Коллаж 3 фото + slide-in | Один hero: cover_green_dragon_clean 700×948, center y=400 |
| Голос громкость | loudnorm I=-16 (голос тонул в музыке) | loudnorm → volume=2.0 (+6dB), музыка 0.10→0.06 |
| Sidechain | ratio=14, attack=8, release=400 | ratio=20, attack=5, release=300 (тighter duck) |
| Обложки PNG | colorkey=white (старые PNGs с белым фоном) | Нет colorkey (чистый RGBA transparent) |

## ⚠️ Технические нюансы для следующих сессий

1. **ffmpeg требует libfreetype** для drawtext — стандартный `brew install ffmpeg` не включает его. Нужен `homebrew-ffmpeg/ffmpeg/ffmpeg` тап (включает freetype + libass). Установлен 2026-05-19.
2. **filter_complex_script deprecated** в ffmpeg 8.x → использовать `-/filter_complex path.txt`
3. **PTS-shift overlay** (setpts=PTS-STARTPTS+T/TB) — правильный способ позиционировать клипы во времени без enable= на каждом overlay
4. **loop filter size** = clip_duration × fps (после нормализации fps=30)
5. **.mcp.json** в video-edits/ — Pexels API ключ действующий. Pexels B-roll workflow: curl API → скачать 1080×1920 link → включить в filter
6. **loudnorm + volume boost формула:** target = final_LUFS - boost_dB. Для voice -14 LUFS с +6dB boost → loudnorm I=-20:TP=-7.5
7. **eof_action=pass** на overlay для loop1 PNG clips с trim — иначе frozen frame после конца клипа
