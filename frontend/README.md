# Zenni Optical — лендинг

Одностраничный лендинг на Vue 3 + Vite для тестового задания по бренду **Zenni Optical**.

## Что на странице

- Название/логотип бренда (кастомный SVG-значок `zenni`)
- Hero-блок с коротким питчем ("Очки от $6.95…") и буллетами доверия
- Секция "Почему Zenni" (3 фичи)
- "Как это работает" — 3 шага
- Отзывы клиентов
- Финальный CTA-баннер
- 5 отдельных CTA-кнопок, у каждой свой `sub1` (`header_nav`, `hero_primary`,
  `hero_secondary`, `how_it_works`, `final_primary`, `final_secondary`), чтобы
  клики можно было различить в `/clicks` / `/dashboard`
- Адаптивная вёрстка (desktop + mobile, проверено до 375px)

## Аналитика (GA4 / GTM) — через env, без хардкода

Раньше ID GA4/GTM были вписаны прямо в `index.html`. Теперь они полностью
берутся из переменных окружения и подключаются динамически в
`src/analytics.js` (вызывается из `src/main.js`):

- `VITE_GA_ID` — Measurement ID GA4 (например, `G-XXXXXXXXXX`)
- `VITE_GTM_ID` — Container ID Google Tag Manager (например, `GTM-XXXXXXX`)

Если переменная не задана — соответствующий скрипт просто не грузится
(никаких плейсхолдеров вида `G-XXXXXXXXXX` в проде). Заполни их в `.env`
(локально) или в Environment Variables хостинга (см. `.env.example`).

**Трекинг кликов по CTA:** каждая CTA-кнопка вызывает `fireCta(sub1, label)`
(`src/config.js`), который до перехода на бэкенд пушит событие `cta_click`
в `window.dataLayer`:

```js
dataLayer.push({ event: 'cta_click', cta_id: sub1, cta_label: label, offer: 'Zenni Optical' });
```

В GTM создай **Custom Event trigger** на `cta_click` и GA4 Event тег, который
срабатывает по этому триггеру (параметры события — `cta_id` / `cta_label`).
Дополнительный код на фронте для этого не нужен.

## Как CTA связаны с бэкендом

CTA-кнопки никогда не ведут напрямую на zennioptical.com. Они вызывают
`fireCta()`, который отправляет браузер на:

```
{VITE_BACKEND_URL}/click?offer=Zenni%20Optical&sub1=<id кнопки>
```

Бэкенд (см. `../backend`) логирует клик и делает 302-редирект на реальный
сайт. Вся логика — в `src/config.js`.

## Запуск локально

```bash
npm install
npm run dev
```

По умолчанию CTA-кнопки смотрят на `http://127.0.0.1:8000` (локальный
бэкенд). Запусти бэкенд из `../backend` рядом, чтобы весь флоу работал
целиком.

Если хочешь локально проверить и аналитику — скопируй `.env.example` в
`.env`, впиши туда `VITE_GA_ID` / `VITE_GTM_ID` и перезапусти `npm run dev`.

## Запуск через Docker

```bash
cd frontend
docker build -t zenni-frontend \
  --build-arg VITE_BACKEND_URL=http://localhost:8000 \
  --build-arg VITE_GA_ID=G-XXXXXXXXXX \
  --build-arg VITE_GTM_ID=GTM-XXXXXXX \
  .
docker run -p 8080:80 zenni-frontend
```

Все `VITE_*`-переменные вшиваются в статическую сборку на этапе `docker
build` (переменные Vite — compile-time, не runtime), поэтому для прода
передавай их через `--build-arg`. GA/GTM аргументы необязательны — если не
передать, эти скрипты просто не подключатся. Либо запусти всё разом через
`docker compose up` из корня проекта — см. `README.md` в корне.

## Сборка и деплой

```bash
npm run build       # статика собирается в dist/
```

1. Скопируй `.env.example` в `.env.production`, укажи `VITE_BACKEND_URL`
   (URL задеплоенного бэкенда) и при желании `VITE_GA_ID` / `VITE_GTM_ID`,
   затем пересобери `npm run build`.
2. Задеплой `dist/` на любой статический хостинг — у Vercel, Netlify, GitHub
   Pages, Cloudflare Pages есть бесплатные тарифы: команда сборки
   `npm run build`, папка публикации `dist`.

### Деплой на Vercel

1. Импортируй репозиторий в Vercel → **Add New Project**.
2. Т.к. это монорепо, в настройках проекта укажи **Root Directory: `frontend`**
   — Vercel сам определит фреймворк (Vite) и подставит команды сборки.
3. В **Settings → Environment Variables** добавь `VITE_BACKEND_URL` (обязательно)
   и при желании `VITE_GA_ID` / `VITE_GTM_ID`.
4. Deploy. При изменении переменных после первого деплоя нужен **Redeploy**
   (переменные вшиваются в бандл при сборке, а не читаются в рантайме).
