# Тестовое задание — лендинг Zenni Optical + бэкенд для трекинга кликов

Выбранный бренд: **Zenni Optical**.

```
project/
  frontend/   Лендинг на Vue 3 + Vite
  backend/    Сервис трекинга кликов на FastAPI + SQLite
```

## Как это работает целиком

```
Пользователь кликает по CTA на лендинге
  -> dataLayer.push({event: 'cta_click', ...})      (трекинг GTM/GA4)
  -> браузер переходит на бэкенд GET /click?offer=Zenni Optical&sub1=<id>
  -> бэкенд генерирует click_id, сохраняет клик в SQLite
  -> бэкенд отвечает 302 -> https://www.zennioptical.com
```

`GET /clicks` на бэкенде отдаёт все сохранённые клики в JSON, а
`GET /dashboard` — ту же информацию, но в виде красивой HTML-страницы со
статистикой (см. `backend/README.md`).

## Стек и инструменты

- **Фронтенд:** Vue 3 (Composition API, `<script setup>`), Vite, чистый CSS
  с дизайн-токенами (без UI-кита) — подробнее в `frontend/README.md`.
- **Бэкенд:** Python, FastAPI, SQLite (`sqlite3` из стандартной библиотеки) —
  подробнее в `backend/README.md`.
- **Контейнеризация:** Docker + Docker Compose (`docker-compose.yml`,
  `backend/Dockerfile`, `frontend/Dockerfile`) — для запуска одной командой
  локально и для деплоя через контейнеры.
- **Аналитика:** GA4 (`gtag.js`) и Google Tag Manager подключаются
  динамически в `frontend/src/analytics.js` на основе переменных окружения
  `VITE_GA_ID` / `VITE_GTM_ID` — никаких ID не зашито в коде.

## Запуск всего локально

```bash
# терминал 1 — бэкенд
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# терминал 2 — фронтенд
cd frontend
npm install
npm run dev
```

Открой адрес, который выведет Vite (обычно `http://127.0.0.1:5173`), кликни
по любому CTA и проверь `http://127.0.0.1:8000/dashboard` — там будет виден
сохранённый клик.

## Запуск всего через Docker

Весь стек (бэкенд + фронтенд, уже связанные между собой) можно поднять
одной командой из корня проекта:

```bash
docker compose up --build
```

Это соберёт и запустит:

- **backend** — FastAPI в контейнере `python:3.12-slim`, на `localhost:8000`,
  `clicks.db` хранится в именованном volume (`clicks_data`), чтобы данные
  переживали перезапуск.
- **frontend** — Vue-приложение собирается в контейнере `node:20-alpine`, а
  раздаётся статикой через `nginx:1.27-alpine` на `localhost:8080`. Собирается
  с `VITE_BACKEND_URL=http://localhost:8000` (см. `docker-compose.yml`), т.к.
  к бэкенду обращается именно браузер, а не контейнер фронтенда — поэтому
  нужен URL, доступный с хоста, а не внутреннее имя сервиса `backend`.

Открой `http://localhost:8080`, кликни по CTA, затем проверь
`http://localhost:8000/dashboard`, чтобы увидеть клик в списке.

Чтобы направить задеплоенный через Docker фронтенд на бэкенд, поднятый
где-то ещё (например, на Render), поменяй `args.VITE_BACKEND_URL` в
`docker-compose.yml` перед `docker compose up --build`, либо собери образ
`frontend` отдельно с `--build-arg VITE_BACKEND_URL=...` (и при желании
`--build-arg VITE_GA_ID=...` / `--build-arg VITE_GTM_ID=...` — см.
`frontend/README.md`).

У каждого сервиса есть свой отдельный `Dockerfile`, если нужно собирать
или деплоить их независимо (`backend/Dockerfile`, `frontend/Dockerfile`) —
большинство хостингов контейнеров (Render, Railway, Fly.io) умеют деплоить
прямо из них, без buildpacks.

## Деплой в публичный доступ

- **Бэкенд:** задеплой `backend/` на Render/Railway/Fly.io (бесплатный тариф) —
  пошагово в `backend/README.md`. `Procfile` уже включён.
- **Фронтенд:** задай `VITE_BACKEND_URL` (URL задеплоенного бэкенда), при
  желании `VITE_GA_ID` / `VITE_GTM_ID`, собери `npm run build` и задеплой
  `frontend/dist/` на Vercel/Netlify/GitHub Pages — пошагово, включая
  настройку Vercel для монорепо, в `frontend/README.md`.

## Аналитика

`frontend/src/analytics.js` подключает GA4 (`gtag.js`) и контейнер Google Tag
Manager (плюс `<noscript>`-фолбэк для GTM), но **только если заданы**
переменные окружения `VITE_GA_ID` и/или `VITE_GTM_ID` — без них скрипты
просто не грузятся, никаких плейсхолдеров вида `G-XXXXXXXXXX` в проде.
Задать их можно в `.env` (см. `frontend/.env.example`) или как Environment
Variables на хостинге (Vercel и т.п.).

Клики по CTA пушат кастомное событие `cta_click` в `dataLayer` с
`cta_id`/`cta_label`/`offer` перед редиректом, так что GTM/GA4 может
отслеживать вовлечённость по кнопкам без дополнительного кода — достаточно
завести Custom Event trigger на `cta_click` в GTM.

## Что делает бэкенд

- `GET /click` — читает query-параметры `offer` + `sub1`, генерирует
  `click_id` (`uuid4`), сохраняет `click_id, offer, sub1, timestamp, ip,
  user_agent` в таблицу `clicks` в SQLite, затем делает `302`-редирект на
  реальный сайт соответствующего бренда (словарь `OFFERS` покрывает все 10
  брендов из задания, сравнение без учёта регистра; неизвестные офферы
  падают на Zenni Optical по умолчанию).
- `GET /clicks` — все строки из `clicks`, сначала новые, в JSON.
- `GET /dashboard` — то же самое, но в виде HTML-страницы со статистикой
  и автообновлением.
- CORS открыт полностью, т.к. фронтенд задеплоен отдельно как статический сайт.

Проверено локально целиком (Playwright): клик по CTA на запущенном фронтенде
доходит до бэкенда, в `/clicks` появляется строка с правильными
`offer`/`sub1`, а браузер оказывается на `zennioptical.com`.
