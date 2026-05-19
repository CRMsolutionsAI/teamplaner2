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

## ⚠️ Технические нюансы для следующих сессий

1. **ffmpeg требует libfreetype** для drawtext — стандартный `brew install ffmpeg` не включает его. Нужен `homebrew-ffmpeg/ffmpeg/ffmpeg` тап (включает freetype + libass). Установлен 2026-05-19.
2. **filter_complex_script deprecated** в ffmpeg 8.x → использовать `-/filter_complex path.txt`
3. **PTS-shift overlay** (setpts=PTS-STARTPTS+T/TB) — правильный способ позиционировать клипы во времени без enable= на каждом overlay
4. **loop filter size** = clip_duration × fps (после нормализации fps=30)
5. **.mcp.json** в video-edits/ — Pexels API ключ действующий. Pexels B-roll workflow: curl API → скачать 1080×1920 link → включить в filter
