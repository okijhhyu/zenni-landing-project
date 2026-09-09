# Бэкенд для трекинга кликов

Сервис на FastAPI + SQLite для CTA-кнопок лендинга.

```
CTA (фронтенд) -> GET /click?offer=<бренд>&sub1=<параметр>
    -> генерирует click_id
    -> сохраняет click_id, offer, sub1, timestamp, ip, user_agent в SQLite
    -> 302-редирект на официальный сайт бренда
```

## Эндпоинты

- `GET /click?offer=Zenni Optical&sub1=hero_primary`
  Логирует клик и делает 302-редирект на реальный сайт бренда.
  `offer` сравнивается без учёта регистра со словарём `OFFERS` в `main.py`
  (покрывает все 10 брендов из задания), так что один и тот же бэкенд
  подходит для лендинга любого из этих брендов.
- `GET /clicks`
  Все сохранённые клики в JSON, сначала новые.
- `GET /dashboard`
  Человекочитаемая HTML-страница со статистикой и таблицей кликов
  (автообновление раз в 15 секунд).
- `GET /`
  Health check.

## Запуск локально

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate   # опционально, но желательно
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Затем:

```bash
curl -i "http://127.0.0.1:8000/click?offer=Zenni%20Optical&sub1=test123"
curl "http://127.0.0.1:8000/clicks"
```

Открой в браузере `http://127.0.0.1:8000/dashboard`, чтобы увидеть клики
в красивом виде.

Файл `clicks.db` (SQLite) создаётся автоматически рядом с `main.py` при
первом запуске.

## Запуск через Docker

```bash
cd backend
docker build -t zenni-backend .
docker run -p 8000:8000 zenni-backend
```

Либо просто `docker compose up` из корня проекта — см. `README.md` в корне.

## Деплой (бесплатные варианты)

Подойдёт любой Python-хостинг. Быстрее всего — бесплатный тариф Render:

1. Запушь папку `backend/` в репозиторий на GitHub (можно и весь проект целиком).
2. На [render.com](https://render.com) → **New Web Service** → подключи репозиторий.
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     (в проекте есть `Procfile` с той же командой, так что Render/Heroku-подобные
     платформы могут определить её автоматически)
3. Задеплой. Render выдаст публичный URL вида `https://your-app.onrender.com`.
4. Укажи этот URL в переменной `VITE_BACKEND_URL` фронтенда (см.
   `frontend/.env.example`) и пересобери фронт.

Railway, Fly.io или PythonAnywhere работают так же — установить
`requirements.txt`, запустить команду uvicorn, открыть порт. Render, Railway
и Fly.io также умеют деплоить прямо из приложенного `Dockerfile`, если
buildpacks не нужны.

## Заметки по реализации

- `click_id` — `uuid4`, хранится как primary key.
- SQLite используется для персистентности без лишней настройки; в таблице
  `clicks` одна строка на клик: `click_id, offer, sub1, timestamp, ip, user_agent`.
- CORS полностью открыт (`allow_origins=["*"]`), т.к. фронтенд — статический
  сайт на другом домене, а наружу торчат только GET-эндпоинты без кук.
- `ip` берётся из `X-Forwarded-For` (его подставляет большинство PaaS-прокси),
  при локальном запуске — из прямого соединения.
- `/dashboard` рендерит HTML прямо в Python (без шаблонизатора и внешних
  зависимостей) — таблица кликов, счётчики по офферу/CTA, автообновление
  через `<meta http-equiv="refresh">`.
