# PROGRESS — Видео-монтаж сессия

## Что сделано

### 1. Wispr Flow промо-ролик (ФИНАЛ ✅)
- **Файл:** `/tmp/wispr_v9.mp4` (64с, вертикаль 1080x1920)
- **Источник:** `/tmp/in.mp4` (1660x1080, 75с) + `/tmp/subs.srt`
- **Статус:** одобрен пользователем («великолепно! спасибо»)
- **Что внутри:**
  - Заставка drawtext (без AI-картинки — по просьбе)
  - Showfreqs equalizer 1080x320 оранжевый (#FF5722)
  - Sidechain ducking музыки под голос (threshold=0.02, ratio=14)
  - Зум на чат+input в окне 43–56с (демо надиктовки)
  - SFX точно по моментам появления текста (28 шт. в `/tmp/sfx/`)
  - Финальная карточка «с Вами была Наталья Седова» + «сделано с помощью АИ»

### 2. Planner туториал (ДОСТАВЛЕНО, без фидбэка)
- **Файл:** `/tmp/plan_final.mp4` (13:06, горизонталь 1920x1080)
- **Источник:** `/tmp/plan_in.mp4` (2072x1080, 13мин)
- **Filter script:** `/tmp/plan_filter.txt` (40 строк, drawtext-оверлеи)
- **Музыка:** `/tmp/plan_music.aac` (866с, 3 трека «Глубокое погружение» с кроссфейдом)

### 3. База знаний референсов
- **Файл:** `/tmp/refs_knowledge.md`
- **Что внутри:**
  - 11 проанализированных референс-видео (стили, тайминги, техники)
  - 9 техник оформления субтитров (размытая подложка, iOS highlighter, подвижная, пиксельная, съехавшая, размытые фигуры, чёрная тонкая обводка)
  - 3 пастельные палитры (оливковый+розовый, лимонный+фисташковый, лаймовый+сливовый)
  - 2 техники монтажа (нумерованный хук, hand-drawn план)
  - Сводная шпаргалка-выбор подложки по стилю
  - Каталог 28 SFX + музыка по категориям + шрифты

## Важные пути

### Источники
| Путь | Что | Размер |
|---|---|---|
| `/tmp/in.mp4` | Wispr Flow исходник | 1660x1080, 75с |
| `/tmp/subs.srt` | Wispr Flow субтитры | — |
| `/tmp/plan_in.mp4` | Planner исходник | 2072x1080, 13мин |
| `/tmp/music.mp3` | Wispr Flow музыка (Позитивное) | b6e2673f |
| `/tmp/music2.mp3` | Глубокое погружение | da85ec67, 325с |

### Ассеты
| Путь | Что |
|---|---|
| `/tmp/avatar.png` | AI-микрофон-аватарка (512x512, из SVG) |
| `/tmp/avatar.svg` | Исходник аватарки (синий градиент) |
| `/tmp/intro_bg.png` | SVG-фон с волной (1080x1920) |
| `/tmp/intro_bg.svg` | Исходник фона |
| `/tmp/fonts/Caveat.ttf` | Handwriting Cyrillic |
| `/tmp/sfx/` | 28 звуковых эффектов |

### Финальные результаты
| Путь | Что |
|---|---|
| `/tmp/wispr_v9.mp4` | ✅ ФИНАЛ Wispr Flow |
| `/tmp/plan_final.mp4` | ✅ Planner туториал |
| `/tmp/plan_filter.txt` | Filter_complex Planner |
| `/tmp/refs_knowledge.md` | База знаний |

## Параметры стиля (бренд)

### Цвета
- **Основной оранжевый:** `#FF5722` (drawtext, equalizer, highlighter)
- **Чёрный + белый** как база
- **Альтернативный жёлтый акцент:** `0xFFEB3B@0.7` (iOS highlight)
- **Пастельные пары** (если lifestyle): см. `refs_knowledge.md`

### Шрифты
- **Display:** Roboto Condensed Bold (`$RCB`)
- **Body:** DejaVu Sans / DejaVu Sans Bold
- **Handwriting:** Caveat (`/tmp/fonts/Caveat.ttf`)

### Музыка по теме
| Категория | Когда |
|---|---|
| Позитивное / Как сейчас всё хорошо | Энергия, продукт-демо |
| Глубокое погружение | Инсайт, обучение, интеллект |
| Сопереживание | Личные истории |
| История любви | Эмоциональные ролики |

## Ключевые ffmpeg-паттерны (для следующих видео)

### Showfreqs equalizer
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
drawtext=...:fontcolor=0xFFFFFF  # текст поверх
```

### Speed-up с синхронизированным звуком
```
[v]setpts=PTS/1.25[vfast]
[a]atempo=1.25[afast]
```

### Subtitle ASS (libass)
- PlayResX=384 по умолчанию — Fontsize в скрипт-юнитах (Fontsize=12 ≈ 60px при 1080)
- BorderStyle=3 (box), BackColour для подложки

## Что осталось / открыто

### Невыполненное
- **Planner v1 без фидбэка** — пользователь не комментировал, можно итерировать
- **Не применены к новому видео** техники из последней пачки 10 картинок (отрисованы в refs_knowledge.md, но не использованы)

### Возможные направления
1. Сделать v2 Planner с iOS-highlighter / multi-size заголовками
2. Применить пастельные палитры к lifestyle-видео
3. Применить «нумерованный хук» (3, 5, 7…) к листам-форматам
4. Hand-drawn план на бумаге для обучающих роликов

### Технический долг
- `/tmp/plan_filter.txt` стоит вынести в шаблон-генератор (питон/баш) для повторного использования
- SFX-каталог `/tmp/sfx/` без индекса — стоит сделать `sfx_index.md` с описанием каждого звука

## Команды-шорткаты

```bash
# Установка переменных шрифтов
RCB=/usr/share/fonts/truetype/roboto/RobotoCondensed-Bold.ttf
DJV=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf
CAV=/tmp/fonts/Caveat.ttf

# SVG → PNG
rsvg-convert -w 1080 -h 1920 /tmp/intro_bg.svg -o /tmp/intro_bg.png

# Длительность файла
ffprobe -v error -show_entries format=duration -of csv=p=0 FILE

# Размер кадра
ffprobe -v error -select_streams v -show_entries stream=width,height -of csv=p=0 FILE
```
