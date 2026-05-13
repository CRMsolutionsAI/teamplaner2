# 🚀 TeamPlanner — Деплой на GitHub + Vercel

## Что нужно
- GitHub аккаунт — github.com ✅ (уже есть)
- Vercel аккаунт — vercel.com (бесплатный)
- Supabase аккаунт — supabase.com (бесплатный)

---

## ШАГ 1 — Supabase (5 минут)

### 1.1 Создать проект
1. Зайдите на **supabase.com** → Sign Up
2. **New project** → название `teamplanner` → придумайте пароль → **Create**
3. Подождите 2 минуты пока создаётся

### 1.2 Создать таблицы
1. В Supabase → **SQL Editor** → **New query**
2. Вставьте содержимое файла `supabase-setup.sql`
3. Нажмите **Run ▶** → должно появиться "Success"

### 1.3 Скопировать ключи
1. **Settings** → **API**
2. Скопируйте и сохраните:
   - **Project URL** → `https://xxxxx.supabase.co`
   - **anon public** key → `eyJhbGc...`

---

## ШАГ 2 — GitHub (3 минуты)

### 2.1 Открыть репозиторий
Зайдите на: **github.com/CRMsolutionsAI/teamplaner2**

### 2.2 Структура файлов

```
├── index.html
├── package.json
├── vite.config.js
├── supabase-setup.sql
└── src/
    ├── main.jsx
    ├── supabase.js
    └── TeamPlanner.jsx   ← САМЫЙ ВАЖНЫЙ
```

---

## ШАГ 3 — Vercel (3 минуты)

### 3.1 Создать аккаунт
1. Зайдите на **vercel.com**
2. Нажмите **Sign Up** → **Continue with GitHub**
3. Разрешите доступ к GitHub

### 3.2 Импортировать проект
1. На главной Vercel → **Add New Project**
2. Найдите **CRMsolutionsAI/teamplaner2** → **Import**
3. Framework Preset: выберите **Vite**

### 3.3 Добавить переменные окружения
Нажмите **Environment Variables** и добавьте 2 переменные:

| Name | Value |
|------|-------|
| `VITE_SUPABASE_URL` | `https://xxxxx.supabase.co` |
| `VITE_SUPABASE_ANON_KEY` | `eyJhbGc...` |

### 3.4 Задеплоить
1. Нажмите **Deploy**
2. Подождите 2-3 минуты
3. Получите ссылку вида: `teamplaner2.vercel.app` 🎉

---

## ШАГ 4 — Доступ по email (опционально)

Чтобы только определённые люди могли войти:

1. В Vercel → ваш проект → **Settings** → **Deployment Protection**
2. **Vercel Authentication** → **Enable**
3. Настройте список email адресов

ИЛИ используйте Cloudflare Access (бесплатно до 50 пользователей):
1. cloudflare.com → Zero Trust → Access → Applications
2. Добавьте домен `teamplaner2.vercel.app`
3. Policy → Allow → Emails → добавьте адреса команды

---

## Проверка работы

После деплоя откройте ссылку и проверьте:
- ✅ Показывается экран "Выберите кто вы"
- ✅ После выбора — открывается планировщик
- ✅ Данные сохраняются после F5
- ✅ Открыть в двух вкладках — видны оба пользователя онлайн

Если что-то не работает:
1. Vercel → ваш проект → **Functions** → смотрите логи
2. Проверьте правильность переменных окружения
3. Supabase → **Table Editor** → таблицы `storage` и `activity_logs` должны существовать

---

## При обновлении кода

Когда обновится `TeamPlanner.jsx`:
1. GitHub → `src/TeamPlanner.jsx` → нажмите карандаш ✏️ → вставьте новое содержимое → Commit
2. Vercel автоматически передеплоит за 2 минуты
