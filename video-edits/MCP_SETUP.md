# MCP Connectors Setup

Подключение коннекторов Pexels, Pixabay, Brave Search к Claude Code (десктоп).

## Что эти коннекторы дадут

| Коннектор | Что делает | Когда применять |
|---|---|---|
| **Brave Search** | Веб-поиск + image search | Найти референсы, проверить факты, поискать примеры монтажа |
| **Pexels** | Stock-видео + фото HD | Кадры B-roll когда не хватает (ночной рынок, паспорта, путешествия) |
| **Pixabay** | Stock-фото + видео + музыка | Альтернативный сток + специфичные кадры |

После подключения я смогу: «найди video паспорта 4K на Pexels» → я ищу, скачиваю, вставляю в монтаж.

## Шаг 1 — Получить API ключи (бесплатно)

### Brave Search
1. https://brave.com/search/api/
2. Sign up → создать **free plan** (2000 запросов/месяц)
3. Скопировать API key

### Pexels
1. https://www.pexels.com/api/
2. Sign up → "Your API Key" в dashboard
3. **Free**: 200 req/час, 20 000 req/месяц

### Pixabay
1. https://pixabay.com/api/docs/
2. Sign up → пользовательская страница → API key
3. **Free**: без жёстких лимитов

## Шаг 2 — Установить Node.js и uv (если ещё нет)

На Mac (Homebrew):
```bash
brew install node uv
```

`node` нужен для Brave Search MCP, `uv` для Pexels и Pixabay (Python-based).

## Шаг 3 — Создать `.mcp.json` из шаблона + вставить ключи

В репо лежит шаблон `.mcp.json.example`. Скопируй его в реальный `.mcp.json` и заполни ключи:

```bash
cd video-edits
cp .mcp.json.example .mcp.json
# Открой .mcp.json и замени YOUR_*_API_KEY_HERE на свои ключи
```

**`.mcp.json` уже в `.gitignore`** — реальные ключи не попадут в репо.

```json
{
  "mcpServers": {
    "brave-search": {
      "env": {
        "BRAVE_API_KEY": "BSA_xxxxxxxxxxxxxxxxxxxxxx"
      }
    },
    "pexels": {
      "env": {
        "PEXELS_API_KEY": "563492ad6f917000010000xxxx"
      }
    },
    "pixabay": {
      "env": {
        "PIXABAY_API_KEY": "12345678-xxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

⚠️ **НЕ коммить `.mcp.json` с реальными ключами в git!** Используй `.gitignore` (см. ниже).

## Шаг 4 — Защитить от случайного коммита

В корне репо или в `video-edits/` добавь к `.gitignore`:
```
.mcp.json
```

ИЛИ — лучший вариант — **держи ключи в env-переменных** на Mac:

```bash
# В ~/.zshrc или ~/.bashrc
export BRAVE_API_KEY="BSA_..."
export PEXELS_API_KEY="..."
export PIXABAY_API_KEY="..."
```

И в `.mcp.json` использовать ссылки на env:
```json
"env": { "BRAVE_API_KEY": "${BRAVE_API_KEY}" }
```

Тогда `.mcp.json` можно безопасно коммитить (там нет ключей).

## Шаг 5 — Запустить Claude Code в папке

```bash
cd ~/Documents/projects/teamplaner2/video-edits
claude
```

При первом запуске Claude Code предложит **доверять MCP серверам** из `.mcp.json` — ответь yes.

## Шаг 6 — Проверка

В сессии Claude скажи:
> «Проверь что MCP работают — найди на Pexels 3 видео по запросу `night market thailand`»

Если работает, я выдам список с превью + сразу могу скачать понравившийся.

## Шаг 7 (опционально) — Если пакеты Pexels/Pixabay не работают

Если `mcp-server-pexels` или `mcp-pixabay` не находятся (community-пакеты могут меняться), есть запасной вариант — я могу написать собственные Python-обёртки за 5 минут. Скажи мне в сессии.

## Что я смогу делать когда коннекторы заработают

```
Ты: «Не хватает B-roll лотоса для secции M4. Найди на Pexels».
Я: → search Pexels API → возвращаю 5 вариантов с превью
Ты: «Третий».
Я: → скачиваю mp4 → сохраняю в footage/ → встраиваю в v_final.mp4
```

Workflow ускорится в разы.

## Возможные проблемы и решения

| Проблема | Решение |
|---|---|
| «MCP server failed to start» | Проверить что Node.js/uv установлены (`node --version`, `uv --version`) |
| «401 Unauthorized» | Перепроверить API ключи. Скопировать заново |
| «Rate limit exceeded» | Подождать (Brave: час, Pexels: 1 час, Pixabay: обычно ОК) |
| Пакет не найден | Использовать запасной вариант (Step 7) |
