# INVENTORY.md — Полный каталог ассетов проекта

## music/ (28MB)

| Файл | Описание | Использовано в |
|---|---|---|
| `wispr_positive.mp3` | Категория «Что-то позитивное» / «Как сейчас всё хорошо», ID `b6e2673f` | Wispr Flow v9 |
| `deep_immersion_track1.mp3` | Категория «Глубокое погружение», ID `da85ec67`, 325с | Wispr Flow v6+ |
| `planner_chained_866s.aac` | Цепочка из 3 треков «Глубокое погружение» с кроссфейдом, 14:26 | Planner туториал |
| `whoosh.wav` | Whoosh из исходника in.mp4 | — |

**Важно:** музыка от пользователя из её собственной библиотеки. Использовать только в рамках её проектов.

## sources/ (39MB)

| Файл | Описание |
|---|---|
| `wispr_source.mp4` | Исходник Wispr Flow (1660x1080, 75с) |
| `wispr_subs.srt` | Субтитры Wispr Flow |
| `planner_source.mp4` | Исходник Planner-туториала (2072x1080, 13мин) |

## sfx/ (3.9MB, 28 файлов)

Звуковые эффекты, организованные по типам:

### Whoosh-семейство (резкие/энергичные)
- `whoosh_grainy_1.mp3`, `whoosh_grainy_2.mp3`, `whoosh_grainy_3.mp3` — основные whoosh для текст-ревеалов
- `fast_blow_whoosh.mp3` — быстрый
- `dust_swoosh.mp3`, `dust_whooshes.mp3` — пыльные/мягкие
- `fireball_whoosh.mp3`, `fireball_whoosh_05224.mp3` — мощные

### Перелёты / переходы
- `vylet_1.mp3`, `vylet_2.mp3` — вылет
- `proletai_transition.mp3` — пролёт
- `low_transition_6group.mp3`, `lowfreq_3pack.mp3` — низкочастотные переходы
- `film_title_transition.mp3` — переход в стиле кино-титра
- `trailer_buildup.mp3` — нарастающий
- `trailer_spaceship.mp3` — космический

### Атмосферные
- `puff_smoke_1.mp3`, `puff_smoke_2.mp3` — пых дыма
- `film_humming_flight.mp3` — гул полёта
- `tv_static.mp3` — статика ТВ
- `cartoon_bubble_pop.mp3` — мультяшный хлопок

### Прочие
- `sfx_04295.mp3`, `sfx_04715.mp3` — индексные
- `unnamed_1.mp3` ... `unnamed_5.mp3` — без названий

## references/ (121MB)

Покадровые экстракты из референс-видео, которые Наталья присылала для анализа стиля.

### ref1_dynamics/
Первое референс-видео про динамику монтажа. 15 ключевых кадров (PNG).

### ref2_motion/
Второе референс-видео про движение/зум. 14 кадров с таймштампами в названии.

### ref3_zoom/
Референс по технике зума. 9 кадров.

### ref4_planner_style/
Референс стиля для Planner-туториала. 17 кадров.

### refX_batch5to8/
Партия рефов 5-8 (см. `refs_knowledge.md`):
- `r5/` — Реф 5 «смогу здесь» (дневниковый, сабы в верх-лев углу)
- `r6/` — Реф 6 «оскар и интерстеллар» (коллажный, постеры IP)
- `r7/` — Реф 7 «снять локации» (Wes Anderson, top-down)
- `r8/` — Реф 8 «меня депортировали» (сторителлинг, multi-size)

### refY_subs_techniques/
Партия рефов по техникам субтитров и палитрам (см. `refs_knowledge.md`):
- `v1/` — Размытая подложка
- `v2/` — Подвижная подложка
- `v3/` — Подложка из стикеров
- `v4/` — iOS highlighter
- `v5/` — Обзор трендов сабов
- `v6/` — Чёрная тонкая обводка
- `v7/` — Съехавшая подложка
- `v8/` — Пиксельная подложка
- `v9/` — Размытые геометрические фигуры
- `vA/` — Пастельные палитры
- `vB/` — Нумерованный хук / hand-drawn

## finals/ (33MB)
- `wispr_v9.mp4` — ✅ Финал Wispr Flow (одобрен)
- `plan_final.mp4` — Planner-туториал (без фидбэка)

## assets/ (52KB)
- `avatar.svg` / `avatar.png` — AI-микрофон-аватарка
- `intro_bg.svg` / `intro_bg.png` — фон с волной для интро

## fonts/ (400KB)
- `Caveat.ttf` — handwriting Cyrillic из Google Fonts

## scripts/ (24KB)
- `plan_filter.txt` — filter_complex для Planner (40 строк)
- `plan_list.txt` — concat-лист сегментов Planner
- `wispr_list.txt` — concat-лист сегментов Wispr Flow

## Документация
- `CLAUDE.md` — авто-загрузка контекста
- `PROFILE.md` — профиль Натальи и бренд
- `FEEDBACK.md` — история правок v1→v9
- `PROGRESS.md` — статус + параметры
- `refs_knowledge.md` — техники из всех 11+ референсов
- `INVENTORY.md` — этот файл

## Что НЕ сохранено в репо

**Промежуточные рендеры** Wispr Flow (v1-v8) — больше 100MB суммарно, легко регенерить из `wispr_source.mp4` через скрипты. Если нужны — переcоздать.

**Reference видео-файлы целиком** — пользователь присылал их как inline-материалы Claude. На диск сохранены только покадровые PNG-экстракты в `references/`.

## Total size
~225MB — в пределах нормы для GitHub-репо. Ни один файл не превышает 30MB.
