# CLAUDE.md — Video Edits Project

> **Этот файл Claude Code читает автоматически** при запуске в папке `video-edits/`.
> Содержит весь контекст видео-проекта Натальи Седовой.

## Контекст и кем работаем

Я (Claude) помогаю Наталье Седовой монтировать короткие и длинные видео.
Стиль — **бренд:** чёрный + белый + оранжевый `#FF5722`.
Шрифты: **Roboto Condensed Bold** (display) + **DejaVu Sans** (body) + **Caveat** (handwriting).

## Что лежит в этой папке

| Файл/папка | Что |
|---|---|
| `PROFILE.md` | Профиль Натальи: бренд, стиль общения, эмоциональные триггеры |
| `FEEDBACK.md` | Хронология её правок + правила «что НЕ повторять» |
| `PROGRESS.md` | Статус: что сделано, что осталось, все параметры |
| `refs_knowledge.md` | База знаний 11 референсов + 9 техник сабов + 3 пастельных палитры |
| `scripts/plan_filter.txt` | filter_complex для Planner-туториала |
| `scripts/wispr_list.txt` | Concat-лист сегментов Wispr Flow |
| `scripts/plan_list.txt` | Concat-лист сегментов Planner |
| `assets/` | SVG-исходники аватара и фона + рендеры PNG |
| `finals/wispr_v9.mp4` | ✅ ФИНАЛ Wispr Flow (одобрен) |
| `finals/plan_final.mp4` | Planner туториал (13:06) |
| `sfx/` | 28 звуковых эффектов |
| `fonts/Caveat.ttf` | Handwriting Cyrillic |

## Первое, что делать в новой сессии

**Обязательно прочитать в таком порядке:**

1. **`PROFILE.md`** — кто клиент, бренд, как общаться, эмоциональные триггеры
2. **`FEEDBACK.md`** — история правок и правил «что НЕ повторять»
3. **`PROGRESS.md`** — точный статус: что сделано / что осталось / пути
4. **`refs_knowledge.md`** — техники из 11 референсов + 9 сабов + 3 палитры

Только после этого спросить: к какому видео применяем / что монтируем.

## Чек-лист перед стартом любого нового видео

(из `FEEDBACK.md`, чтобы не повторять старых ошибок)

- [ ] Sidechain ducking настроен? (музыка не громче голоса)
- [ ] Никаких AI-картинок в интро? (только drawtext)
- [ ] Никакого letterbox на вертикали?
- [ ] SFX тайминги точно по тексту (не на 0.1с раньше)?
- [ ] Музыка категорийно соответствует теме речи?
- [ ] Эквалайзер минимум 320px высота?
- [ ] Сайн-офф «С Вами была Наталья Седова + сделано с АИ»?
- [ ] Multi-size заголовки где уместно?
- [ ] Резки минимум каждые 2-4с?

## Бренд и стиль (быстрая шпаргалка)

### Цвета
- Основной оранжевый: `#FF5722` (drawtext, equalizer, highlighter)
- Жёлтый акцент iOS-highlight: `0xFFEB3B@0.7`
- База: чёрный + белый

### Шрифты (системные пути на Mac)
```bash
RCB=/System/Library/Fonts/Supplemental/Roboto-Condensed-Bold.ttf  # или установить
DJV=/System/Library/Fonts/Supplemental/DejaVu\ Sans\ Bold.ttf      # brew install --cask font-dejavu
CAV=./fonts/Caveat.ttf
```

### Музыка по теме
- **Позитивное** → энергия, продукт-демо
- **Глубокое погружение** → инсайт, обучение
- **Сопереживание** → личные истории
- **История любви** → эмоциональные ролики

## Ключевые ffmpeg-паттерны

### Showfreqs equalizer (оранжевый)
```
[a_freq]showfreqs=s=1080x320:mode=bar:colors=0xFF5722:ascale=log:fscale=log:
win_size=2048:cmode=combined:averaging=2,format=yuva420p,
colorchannelmixer=aa=0.95[freq]
```

### Sidechain ducking (музыка под голос)
```
[mraw][key]sidechaincompress=threshold=0.02:ratio=14:attack=8:release=400:
makeup=1:level_sc=2[mducked]
```

### Text fade in/out
```
drawtext=fontfile=$RCB:text='WISPR':fontcolor=0xFFFFFF:fontsize=280:
x=(w-text_w)/2:y=550:enable='between(t,4.5,13)':
alpha='if(lt(t,4.8),(t-4.5)/0.3,if(gt(t,12.5),max(0,1-(t-12.5)/0.5),1))'
```

### iOS highlighter (полоса позади слова)
```
drawbox=x=...:y=...:w=...:h=...:color=0xFF5722@0.7:t=fill
drawtext=...:fontcolor=0xFFFFFF
```

### Speed-up с синхронным звуком
```
[v]setpts=PTS/1.25[vfast]
[a]atempo=1.25[afast]
```

## Что НЕ лежит в репо (нужно перезагрузить локально)

См. **`INVENTORY.md` → раздел «⚠️ ПРОБЕЛЫ»** — там точный список того, что отсутствует.

Кратко:
- **Музыкальные треки** — есть только 2 из 5 категорий. Полная библиотека по категориям отсутствует.
- **Reference mp4 файлы** — есть только PNG-кадры, не сами видео.
- **Промежуточные рендеры Wispr v1-v8** — не нужны, регенерятся из `sources/wispr_source.mp4`.

**В новой сессии:** первым делом спросить Наталью, нужно ли добрать музыкальную библиотеку — и если да, организовать в подпапки `music/{positive,empathy,all_good_now,deep_immersion,love_story}/`.

## Правила работы

1. **Не пушить большие mp4** (>50MB) — лучше регенерить из скриптов
2. **Все финальные видео** идут в `finals/`
3. **Обновлять `PROGRESS.md`** при значимых изменениях
4. **Обновлять `refs_knowledge.md`** когда пользователь даёт новые референсы
5. **Никогда не коммитить** music-файлы (авторские права) — только пути/имена
6. **Шрифты** — Caveat в `fonts/`, остальные системные на Mac

## История одобренных решений

- ❌ AI-генерёные intro-картинки → ✅ drawtext only
- ❌ Маленький showwaves → ✅ showfreqs 1080x320 ярче
- ❌ Музыка громче голоса → ✅ sidechain ducking
- ❌ Letterbox на вертикали → ✅ полный кадр без полос
- ❌ Дешёвая обводка субтитров → ✅ box-стиль
- ❌ Тряска от sin-зума → ✅ статика или zoompan
- ✅ SFX точно на момент появления текста (не на 0.1с раньше)
- ✅ Финальная карточка: «с Вами была Наталья Седова + сделано с помощью АИ»

## Команды быстрого старта

```bash
# Проверить длительность
ffprobe -v error -show_entries format=duration -of csv=p=0 FILE

# Размер кадра
ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=p=0 FILE

# SVG → PNG
rsvg-convert -w 1080 -h 1920 assets/intro_bg.svg -o assets/intro_bg.png
```
