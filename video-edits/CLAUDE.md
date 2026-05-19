# CLAUDE.md — Video Edits

> Авто-подгружается при запуске в `video-edits/`. Только универсальные правила.
> Спецификация проекта — в `projects/<X>/README.md`.

## Первый шаг любой сессии

1. Открыть `projects/<X>/README.md` — там раскадровка + скрипт диктора.
2. Если README нет — попросить пользователя заполнить из `PROJECT_README_TEMPLATE.md`.
3. Только после этого смотреть исходники / монтировать.

## Бренд

- Цвета: **`#FF5722`** (оранжевый) + чёрный + белый
- Шрифты: **Roboto Condensed Bold** (display) · **Roboto-Black** (impact) · **Caveat** (handwriting)
- Формат экспорта: MP4, H.264, **1080x1920** (вертикаль) или 1920x1080 по ТЗ

## Жёсткий каркас

- **Голос диктора = закон.** Длина ролика = длине аудио, ни секундой больше.
- **Порядок сборки:** Аудио → Видеоряд → Эффекты → Графика → QC.

## Premium-визуальная парадигма (default для cinematic-mood)

Эти приёмы установлены через project_002 — выглядят дорого, применяются по умолчанию:

- **«Окно в чёрном»** — видео не full-bleed, а окошко (720x1200 CENTER / 600x1000 LEFT/RIGHT) на чёрном canvas. Текст РЯДОМ с окном, не поверх. Layout-варианты CENTER / LEFT / RIGHT + BLACK для big titles + FULL только на climax-моментах.
- **Fade-in 250мс** для всех drawtext: `alpha='if(lt(t,t0+0.25),(t-t0)/0.25,1)'`
- **Teal-orange цветокор:** `eq=contrast=1.10:saturation=1.10,colorbalance=rs=-0.04:bs=0.05:rm=0.03:bm=-0.04:rh=0.05:bh=-0.05`
- **Music swell** +6dB на 2 key moments (big rule / climax): `volume='0.10+0.06*(between(t,A,B)+between(t,C,D))':eval=frame`
- **Slow-mo 0.5x** на mystical / emotional climax: `trim,setpts=PTS*2.0,fps=30`

## Хук — первые 0-3 секунды

**Visceral или ничего.** Зритель решает за 3 сек, смотрит ли дальше.

✅ Что работает:
- Крупный план (eye / fur texture / face)
- Резкое движение (motion / cut)
- Неожиданный кадр (tiger в бассейне)
- Сильный текст с обещанием пользы (1 правило, X секунд истины)

❌ Что НЕ работает как хук:
- POV-руки на статичной поверхности
- Wide-shot без действия
- Тихое мирное вступление

**Если хук тихий — переделать.** Не пускать в render.

## Аудио-иерархия

```
Голос (0 dB) > SFX (-12…-14 dB) > Музыка (-18…-20 dB)
```
- Музыка всегда от 1-го до последнего кадра (исключение — пауза для эффекта).
- Sidechain ducking: `sidechaincompress=threshold=0.02:ratio=14:attack=8:release=400`.
- SFX: **только на движение** (резка кадра / появление-исчезновение текста). Если ничего не движется — звука нет.
- Никаких длинных riser/buildup/reverse — звучат как «перемотка». SFX ≤ 3.5 секунд.
- **Music swell +6dB на 2-3с** на big-rule и climax (см. premium-paradigm выше).

## Видеоряд

- Резки **под смысловые акценты речи**, не под равные интервалы.
- Резка минимум каждые 2-4с, иначе зритель «уходит».
- Динамика (zoom/pan) только на акцентах, не сплошным потоком.
- **Никакого sin-зума и Ken Burns на handheld-фото** — амплифицирует тряску. Статика или zoompan только на студийных PNG.
- Никакого letterbox на вертикали.
- **Photo policy:** фото = резервный материал, не основной. Используем только если для этого момента **нет видео-альтернативы**. Если фото неизбежно — делаем `photo_zoom` (slow zoompan + 0.08 за длительность), статика выглядит «дёшево».

## Текст

- Короткие фразы, в **safe zone** (top ≥180, bottom ≤1620 для UI соцсетей).
- Каждое появление текста = свой SFX (тише голоса, чуть громче музыки).
- Тайминг от **silencedetect** на голосе, lead -0.15с до фразы.
- Big multi-tier headline на финале (Roboto-Black + Caveat).
- Subtitles в отдельном render-пасе — позволяет править текст без ре-рендера видео.
- **Fade-in 250мс** на каждый drawtext (см. premium-paradigm).
- **Sidebar text constraint:** text в боковой зоне окна (LEFT layout → x>720, RIGHT layout → x<400) — **максимум 5 символов** в Roboto-Black 130+ ИЛИ ширина ≤380px. Если фраза длиннее — выносить TOP (y<420) или BOTTOM (y>1480) full-width.
- **Title-визуал alignment:** каждый title обязан совпадать с тем что в кадре И что говорит голос в этот момент. Если визуала нет — менять title, не закрывать глаза. Проверка на этапе A2 для каждого титра.

## Workflow для итераций

### Этап A — **до рендера**, только текст:

1. **Voice-маркеры** (silencedetect) — присылаю Наталье на подтверждение.
2. **Раскадровка** таблицей (Time | Layout | Source | Voice | Title) — её «ок».
   - **Title-визуал alignment check** для каждой строки таблицы.
3. **Hook предложение:** описание шота + чем цепляет — её «да/нет». Если слабо — переделать ДО любого рендера.
4. **Photo policy:** один вопрос «только видео / видео+фото где нет видео / 50/50» — её выбор.
5. **Footage gallery upfront:** для мастер-клипов длиннее 60с — сэмплирую 8-12 кадров (t=0, 30, 60, ...), присылаю галерею, она помечает «эти беру».
6. **SFX-палитра** списком — её «ок».
7. **Музыка:** спрашиваю mood одним словом (cinematic / playful / emotional / aggressive) → подбираю 1-2 трека.

### Этап B — **рендер слоями**:
8. video_only.mp4 (без текста/звука) → проверка склеек
9. + диктор + музыка → проверка баланса
10. + SFX → проверка акцентов
11. + текст → финал
12. (опционально) pitch-shift для соцсетей

## Самопроверка перед каждой отдачей

**ОБЯЗАТЕЛЬНО** в каждом моём ответе с отправкой видео — секция **«Что ещё могу улучшить»** с 2-4 конкретными точками. Без этого зрителю кажется, что я считаю работу финальной — и она остаётся слабой там где я не подсветил.

Шаблон:
```
## 🔍 Что ещё могу улучшить (по моей оценке v_N)
1. [конкретная проблема] — [как исправить]
2. ...
```

Не льстить себе — критически разбирать. Если всё идеально (редко) — сказать честно «не вижу что улучшить».

## Чек-лист QC

- [ ] Длина ролика = длине аудио
- [ ] Hook visceral в 0-3с (см. хук-правила)
- [ ] Sidechain ducking настроен
- [ ] SFX точно на момент текста (не на 0.1с раньше/позже)
- [ ] Весь текст в safe zone
- [ ] **Sidebar text fits** — прогнать `_utils/check_text_width.py` на text events перед рендером
- [ ] Title-визуал alignment проверен
- [ ] Нет sin-зума и тряски на фото
- [ ] Резки каждые 2-4с
- [ ] Финальная карточка/CTA на чёрном с акцентным шрифтом
- [ ] Музыка категорийно соответствует теме (+ swell на 2 key moments)
- [ ] Fade-in 250мс на все drawtext
- [ ] **После approve:** `lessons_learned.md` заполнен (2-3 plus + 1 техническое усложнение)

## Утилиты

- `_utils/check_text_width.py` — проверяет влезает ли drawtext в свой sidebar/top/bottom slot. Использовать ДО рендера в text_*.py:
  ```python
  from video_edits._utils.check_text_width import check_drawtext
  check_drawtext(text, font, size, x, y, layout="LEFT")  # WARN если overflow
  ```

- `_utils/align_transcript.py` — выравнивает дословный текст транскрипта по `silencedetect` границам в voice.wav. **Запускать ОДИН РАЗ на этапе A1** перед раскадровкой:
  ```
  python3 _utils/align_transcript.py voice.wav sources/transcript.txt
  → [0.66s] Встреча с тигром это не туристический аттракцион
  → [4.06s] В полторах часах от Бангкока...
  ```
  Точный map «фраза → секунда» = титры не промахиваются (как было с «ОТКРЫВАЕТ ЖИВОТ» в project_002).

- `_utils/start_iter.sh` — бустрапит новую итерацию: `./start_iter.sh project_NNN_X vN` → создаёт build dir + WORKFLOW_STATE.md + time_log.md + git commit.

- `_utils/text_script_template.py` — стартер для text_vN.py с интегрированным `check_text_width`, fade-in 250мс, teal-orange grade.

- `_utils/prep_photo.sh` — конвертирует iPhone HEIC → PNG. Опционально `--transparent` для удаления фона (rembg).
  ```
  ./prep_photo.sh photo.HEIC --transparent --output-dir sources/photos/
  ```

- `_utils/shrink_video.sh` — сжимает видео под лимит чат-аплоада (≤30MB).
  ```
  ./shrink_video.sh big_video.mov --target-mb 25 --output compact.mp4
  ```
  Использует two-pass H.264 для точного попадания в bitrate.

## Запреты (из FEEDBACK истории)

- ❌ AI-генерёные intro-картинки → ✅ только drawtext
- ❌ Музыка громче голоса → ✅ sidechain
- ❌ Letterbox на вертикали → ✅ full bleed
- ❌ Длинные SFX (>3.5с) с риз/реверсом → ✅ короткие импакты
- ❌ Стоки на сам продукт → ✅ только её файлы для продукта; стоки только для контекста
- ❌ **`silenceremove` на голосе диктора** → ✅ только `atempo` (естественные паузы оставляем — без них слушать невозможно)
- ❌ **Фото как основной материал** → ✅ фото только для конкретного момента где нет видео, всегда `photo_zoom` (с slow zoompan, не статика)
- ❌ **Слабый POV-хук** (рука на мехе, wide без действия) → ✅ visceral в 0-3с
- ❌ **Sidebar text >5 символов / >380px** → ✅ выносить TOP/BOTTOM full-width
- ❌ **Title не совпадает с визуалом** («ОТКРЫВАЕТ ЖИВОТ» без живота в кадре) → ✅ менять title под визуал ИЛИ искать другой кадр

## ffmpeg-шпаргалка

```bash
# Длительность
ffprobe -v error -show_entries format=duration -of csv=p=0 FILE

# Голос с темпо + loudnorm (НИКАКОГО silenceremove на голосе диктора)
ffmpeg -i voice.ogg -af "atempo=1.20,loudnorm=I=-14:TP=-1.5:LRA=11,volume=1.5dB" voice.wav

# Silencedetect для тайминга субтитров
ffmpeg -i voice.wav -af "silencedetect=noise=-26dB:d=0.12" -f null - 2>&1 | grep silence_end

# Sidechain ducking
[mraw][voice]sidechaincompress=threshold=0.02:ratio=14:attack=8:release=400:makeup=1:level_sc=2[mducked]

# Music swell на 2 key moments
volume='0.10+0.06*(between(t,64,69)+between(t,85,90))':eval=frame

# Teal-orange grade
eq=contrast=1.10:saturation=1.10,colorbalance=rs=-0.04:bs=0.05:rm=0.03:bm=-0.04:rh=0.05:bh=-0.05

# Slow-mo 0.5x
[v]trim,setpts=PTS*2.0,fps=30[v_slow]

# Master mix с лимитером
[v][s][m]amix=inputs=3:duration=first:weights=1.0 1.0 0.6:normalize=0,alimiter=limit=0.95[out]

# Pitch-shift -50 cents (для соцсетей чтоб не банили музыку по copyright fingerprint)
# Math: -50¢ = pitch factor 2^(-50/1200) = 0.9716. Speed compensated by atempo 1.0292.
# ВАЖНО: первый aresample=44100 заставляет filter работать на известном SR (иначе
# если исходник 96kHz/48kHz — asetrate=44100*0.9716 даст драматическое замедление).
# Тестировано на project_002 v_final.mp4 — drift 23мс на 108s, OK.
ffmpeg -i v_final.mp4 -af "aresample=44100,asetrate=44100*0.9716,aresample=44100,atempo=1.0292" \
  -c:v copy v_final_shifted.mp4
```

## Облачные ограничения

- Pexels/Pixabay/Brave CDN **заблокированы из cloud-сессии** (egress allowlist).
- MCP-коннекторы работают только локально на Mac. В облаке — получать файлы через `@`-аплоад.
- Большие исходники (≥30MB chat upload limit / 50MB git limit) — в репо через git push, не через inline.
- **Whisper ASR** — Python пакет установлен, но скачивание моделей openai заблокировано в облаке. `--asr` режим в `align_transcript.py` падает в heuristic fallback. **Используется только на Mac локально.**

## Обработка iPhone/big-file файлов

Когда заказчица присылает HEIC или большое видео:

| Что | Workflow |
|---|---|
| **HEIC фото** | `@`-аплоад → я конвертирую через `_utils/prep_photo.sh` (+ `--transparent` для PNG без фона) → результат в `sources/photos/` |
| **Видео >30MB** | git push (нет лимита) → я подхватываю → если нужно отправить обратно: `_utils/shrink_video.sh --target-mb 25` |
| **Аудио** | `@`-аплоад (обычно <30MB) → в `sources/narrator_audio.*` |

Заказчице **не нужно** ничего конвертировать локально — она кидает оригиналы, я обрабатываю в cloud.

## История проектов

- ✅ `projects/project_001_noface/` — обложка паспорта из Таиланда (v12, 48.6с)
- ✅ `projects/project_002_tiger_park/` — Tiger World, Ратчабури (v5, 108с) — premium-paradigm установлена
- `finals/` — **legacy архив** старых проектов (Wispr Flow, Planner). Новые проекты держат `v_final.mp4` внутри `projects/<X>/`, не переносим.

Для деталей каждого — открыть его `README.md`.

## Workflow tracking (per-project)

В каждой папке `vN_build/` создавать **`WORKFLOW_STATE.md`** (шаблон в `_utils/workflow_state_template.md`) — отмечаю прогресс по гейтам A1→B12. Тебе видно где я сейчас.

В корне каждого проекта вести **`time_log.md`** (шаблон в `_utils/time_log_template.md`) — фиксирую старт/финиш каждой итерации. Метрика «итераций × минут на проект» для бенчмарка прогресса.
