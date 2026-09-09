# Zenni Optical — landing page

Vue 3 + Vite single-page landing for the **Zenni Optical** test-task brief.

## What's on the page

- Brand name/logo (custom SVG mark, `zenni`)
- Hero with a short pitch ("Glasses from $6.95…") and trust bullets
- "Why Zenni" 3-up feature section
- "How it works" 3-step process
- Customer testimonials
- Final CTA banner
- 5 separate CTA buttons, each tagged with its own `sub1` value
  (`header_nav`, `hero_primary`, `hero_secondary`, `how_it_works`,
  `final_primary`, `final_secondary`) so clicks can be told apart in `/clicks`
- Responsive layout (desktop + mobile tested down to 375px)

## Analytics

`index.html` includes both:

- **gtag.js** (GA4) snippet
- **Google Tag Manager** snippet (`<script>` in `<head>` + `<noscript>` in `<body>`)

Replace the placeholder IDs before deploying:

- `G-XXXXXXXXXX` → your GA4 Measurement ID
- `GTM-XXXXXXX` → your GTM Container ID (appears twice: script + noscript)

**CTA tracking:** every CTA button calls `fireCta(sub1, label)`
(`src/config.js`), which pushes a `cta_click` event to `window.dataLayer`
*before* navigating to the backend:

```js
dataLayer.push({ event: 'cta_click', cta_id: sub1, cta_label: label, offer: 'Zenni Optical' });
```

In GTM, create a **Custom Event trigger** on `cta_click` and a GA4 Event tag
that fires on it (map `cta_id` / `cta_label` as event parameters) — no extra
frontend code is needed for that part.

## CTA → backend wiring

CTA buttons never link straight to zennioptical.com. They call
`fireCta()`, which sends the browser to:

```
{VITE_BACKEND_URL}/click?offer=Zenni%20Optical&sub1=<button id>
```

The backend (see `../backend`) logs the click and then 302-redirects to the
real site. See `src/config.js` for the full logic.

## Run locally

```bash
npm install
npm run dev
```

By default the CTA buttons point at `http://127.0.0.1:8000` (the local
backend). Run the backend from `../backend` alongside this for the full flow
to work end to end.

## Run with Docker

```bash
cd frontend
docker build -t zenni-frontend --build-arg VITE_BACKEND_URL=http://localhost:8000 .
docker run -p 8080:80 zenni-frontend
```

`VITE_BACKEND_URL` is baked into the static build at `docker build` time
(Vite env vars are compile-time), so pass your real backend URL as a
`--build-arg` when building for production. Or just use `docker compose up`
from the project root — see the top-level `README.md`.

## Build & deploy

```bash
npm run build       # outputs static files to dist/
```

1. Copy `.env.example` to `.env.production` and set `VITE_BACKEND_URL` to
   your deployed backend's URL, then re-run `npm run build`.
2. Deploy `dist/` to any static host — Vercel, Netlify, GitHub Pages,
   Cloudflare Pages all have free tiers that work by just pointing them at
   this repo/folder with build command `npm run build` and publish
   directory `dist`.
