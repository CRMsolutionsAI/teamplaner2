# Project_001 — Lessons Learned

**Финальная версия:** `v_final.mp4` (53.4с, vertical 1080x1920)
**Дата:** 2026-05-19

## ✅ Что получилось лучше всего

1. **Black canvas + frame-in-frame архитектура** — отказ от full-bleed footage сразу убрал «дешёвое» ощущение. Видео-окна на чёрном фоне работают как design composition, а не «съёмка с телефона».

2. **Heavy text-overlay подход** — каждая секция получила 2-3 текстовых события (display + accent + caption). Каждое слово несёт значение: «СЕЙФ / не сувенир» сильнее любого UI-перехода.

3. **Multi-tier finale** «ВАШ / ПАСПОРТ / — *ваша история*» (Roboto Condensed Bold 200px + Caveat 110px) — один из лучших closing-cards в библиотеке проекта. Reusable pattern для будущих видео.

4. **Аудио-формула работает** — sidechain ducking музыки под голос + 7 SFX-акцентов на резках = голос всегда первый план, музыка дышит, SFX подчёркивает движение. Никаких конфликтов.

5. **Гигантский ценник «120» в оранжевой коробке** (320px) — самый сильный визуальный момент ролика. Reusable приём для любого «hook-with-money-number» контента.

## 🎯 Конкретное усложнение для следующего ролика

**Применить «diagonal scattered text reveal»** (из ref c5b53306 — «ТЕМ СИЛЬНЕЕ ЦЕПЛЯЕШЬ ВНИМАНИЕ ЗРИТЕЛЯ»):
- Каждое слово фразы появляется на разной X-позиции и разной Y-высоте по диагонали
- Время появления слов сдвинуто на 0.15-0.3с каждое
- Финальный кадр — вся фраза собрана, читается как layout

В этом ролике пытался сделать через offset X у слов «НОЧНОЙ» (x=80) и «РЫНОК» (x=320), но это статика. Нужно добавить движение/timing для эффекта «слов-собирающихся».

## 📋 Чек-лист контроля качества

- [x] Нет чёрных экранов и пустот (черный = design background, не пустота)
- [x] Длина ролика = длине аудио (53.4с)
- [x] Иерархия громкости соблюдена (loudnorm -5 LUFS голос, music vol=0.1, sfx vol=0.25)
- [x] Sidechain ducking музыки под голос
- [x] Весь текст в safe zone (top 200px, bottom y≤1620 для Instagram UI запаса)
- [x] Frame-in-frame на черном фоне (без letterbox blur)
- [x] Color grade применён (warm + slight contrast)
- [x] Sign-off pattern Натальи (multi-tier text + handwriting accent)
- [x] Бренд-цвет #FF5722 везде

## 🔁 Использованные техники из библиотеки

| Из refs_knowledge.md | Применено где |
|---|---|
| `refS s124` multi-tier title pattern (Dela Gothic + handwriting) | M5 finale «ВАШ / ПАСПОРТ / — *ваша история*» |
| `refU u13` hook-with-money-number | M4 «ЦЕНА / 120 / БАТ» giant box |
| `refT t126` frame-in-frame layout (per_aspera_ad_astra) | Все 5 секций (offset frames на черном) |
| `refQ` iOS highlighter (drawbox + text) | M3 NATALIA имя в чёрной плашке |
| Audio: sidechain ducking | Wispr v9 паттерн ре-используется |

## 📝 Технические данные

- **Кодек:** H.264, CRF 19, preset medium, AAC 192k
- **Разрешение:** 1080x1920 @ 30fps
- **Длительность:** 53.4с
- **Размер:** 13 MB
- **Музыка:** `all_good_now/aqualina_orange_hues_201s.mp3` (категория «Как сейчас всё хорошо»)
- **SFX:** 7 точек (whoosh_grainy × 3, dust_swoosh × 2, cartoon_bubble_pop, film_title_transition)
- **Шрифты:** Roboto Condensed Bold (display) + Caveat (handwriting) + DejaVu Sans Bold (NATALIA box)
- **Color grade:** `eq=contrast=1.12:saturation=1.08:gamma_r=0.96:gamma_b=1.04`

## ⚠️ Что нужно для следующих видео

1. **Чистые product photos** (с прозрачным фоном) — Наталья пыталась прислать inline, не сохранились. На будущее: всегда attach файл, не paste в чат.
2. **MCP-коннектор для web-поиска стоков** (Brave Search / Pexels / Pixabay) — для случаев когда не хватает кадров и нужны generic-плейсхолдеры.
3. **Whisper или ручные субтитры** — в этом ролике сделал acent-text без полных слов диктора. В следующем можно добавить полные субтитры в safe zone.
