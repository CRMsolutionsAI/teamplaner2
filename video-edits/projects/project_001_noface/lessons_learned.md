# Project_001 — Lessons Learned

**Финальная версия:** `v_final.mp4` v7 (48.6с, vertical 1080x1920, -11.2 LUFS, LRA 3.2)
**Дата:** 2026-05-19

## 🔄 v7 — фиксы по обратной связи Натальи

1. **Премиум-анимации хука (0-6.36с)** — спринг-вход с overshoot (punch-in 1.5→1.0 за 0.5с), slide-in с поворотом -12°, параллакс на финальной паре обложек. xfade между шотами вместо хард-катов.
2. **Субтитры синхронизированы с голосом** — детектил фразовые границы через `silencedetect -30dB`, выровнял каждый текст с lead -0.15с. **Критично:** «120 БАТ» сдвинут с 34.2 → 32.86 (голос произносит «120» на 33.01).
3. **M4 сцена «120» переделана** — black-канвас стартует с 33.01 (синхронно с голосом), а не с 34.0. Большой 380px «120» появляется одновременно с произнесением.
4. **19 разных SFX вместо одного** — каждое движение получило индивидуальный звук из библиотеки sfx/: vylet → dust_swoosh → film_title_transition → cartoon_bubble_pop → puff_smoke → whoosh_grainy → trailer_buildup (на «120 БАТ» — самый сильный) → trailer_spaceship на финале.
5. **Громкость SFX поднята** 0.55 → 0.70-0.90 (varied), общий вес в миксе 0.9 → 1.05.

## ⚠️ Что осталось вне v7

**Стоковые видео (Pexels) — недоступны из cloud-окружения** (egress allowlist блокирует videos.pexels.com). 3 ID были выданы локальным Claude:
- 28515504 (1080x1920 60fps)
- 28515508 «A woman preparing food at a food stand» (5с)
- 30119040 «Street vendor making Thai roti» (30с)

Чтобы добавить в v8: скачать локально и положить в `sources/stock/`, либо передать через repo commit.

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

---

## v6 (2026-05-19) — после фидбека «динамики мало, звуки тихие, паспорт на стоках»

**Ключевые изменения от v5:**
- 19 шотов вместо 13 (avg cut every 2.6s, было 4-5s) — резкая динамика
- Pexels стоки УБРАНЫ полностью. Только её 5 mp4 + 6 PNG обложек
- Аудио микс пересобран: I=-12 LUFS (было -17), LRA=2.4 (было 0.9), SFX vol 0.55 (было 0.25)
- 19 SFX событий (было 7) — звук на каждом cut'е
- Hero PNG covers на черном фоне для M1 hook (вместо клипа продавца)
- Цена «120 БАТ» — только на чёрном с большим оранжевым боксом 380px
- Финал: одна hero PNG (green dragon) + multi-tier title + handwriting CTA
- atempo=1.10 (было 1.09) → 48.6с финал

**Технические нюансы (cloud-render):**
- ffmpeg scale: `force_original_aspect_ratio=increase` для безопасного crop когда zoom меняется
- Сегментная сборка (19 mp4 → concat) удобнее одного гигантского filter_complex
- drawtext filter chain ~6000 chars OK через -vf "$VAR"
- Roboto Condensed Bold + Roboto Black + Caveat — полная поддержка кириллицы
