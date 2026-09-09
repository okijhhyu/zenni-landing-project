# Test task — Zenni Optical landing page + click-tracking backend

Brand chosen: **Zenni Optical**.

```
project/
  frontend/   Vue 3 + Vite landing page
  backend/    FastAPI + SQLite click-tracking service
```

## How it works end to end

```
User clicks a CTA on the landing page
  -> dataLayer.push({event: 'cta_click', ...})      (GTM/GA4 tracking)
  -> browser navigates to backend GET /click?offer=Zenni Optical&sub1=<id>
  -> backend generates click_id, stores the click in SQLite
  -> backend responds 302 -> https://www.zennioptical.com
```

`GET /clicks` on the backend returns every stored click as JSON.

## Stack & tools used

- **Frontend:** Vue 3 (Composition API, `<script setup>`), Vite, plain CSS
  with design tokens (no UI kit) — see `frontend/README.md`.
- **Backend:** Python, FastAPI, SQLite (`sqlite3` stdlib) — see
  `backend/README.md`.
- **Containerization:** Docker + Docker Compose (`docker-compose.yml`,
  `backend/Dockerfile`, `frontend/Dockerfile`) for one-command local runs
  and container-based deploys.
- **Tooling used while building:** Claude (code generation + this write-up),
  Vite/npm and pip for scaffolding and dependencies, Playwright for local
  visual QA (desktop + mobile screenshots) during development.

## Run everything locally

```bash
# terminal 1 — backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# terminal 2 — frontend
cd frontend
npm install
npm run dev
```

Open the printed Vite URL (usually `http://127.0.0.1:5173`), click any CTA,
and check `http://127.0.0.1:8000/clicks` to see the stored click.

## Run everything with Docker

The whole stack (backend + frontend, wired together) can be started with
one command from the project root:

```bash
docker compose up --build
```

This builds and runs:

- **backend** — FastAPI in a `python:3.12-slim` container, on `localhost:8000`,
  with `clicks.db` persisted in a named volume (`clicks_data`) so data
  survives restarts.
- **frontend** — Vue app built inside a `node:20-alpine` stage, then served
  as static files by `nginx:1.27-alpine`, on `localhost:8080`. It's built
  with `VITE_BACKEND_URL=http://localhost:8000` (see `docker-compose.yml`),
  since the browser — not the frontend container — is what calls the
  backend, so it needs a host-reachable URL rather than the internal
  `backend` service name.

Open `http://localhost:8080`, click a CTA, then check
`http://localhost:8000/clicks` to see it logged.

To point the Dockerized frontend at a backend deployed elsewhere (e.g. on
Render), change `args.VITE_BACKEND_URL` in `docker-compose.yml` before
running `docker compose up --build`, or build the `frontend` image
standalone with `--build-arg VITE_BACKEND_URL=...` (see
`frontend/README.md`).

Each service also has its own standalone `Dockerfile` if you want to build
or deploy them independently (`backend/Dockerfile`, `frontend/Dockerfile`) —
most container hosts (Render, Railway, Fly.io) can deploy straight from
these instead of buildpacks.

## Deploying publicly

- **Backend:** deploy `backend/` to Render/Railway/Fly.io (free tier) —
  step-by-step in `backend/README.md`. A `Procfile` is included.
- **Frontend:** set `VITE_BACKEND_URL` to the deployed backend URL, run
  `npm run build`, deploy `frontend/dist/` to Vercel/Netlify/GitHub Pages —
  step-by-step in `frontend/README.md`.

## Analytics confirmation

`frontend/index.html` has both the GA4 (`gtag.js`) snippet and the GTM
container snippet installed, plus a `noscript` GTM fallback. CTA clicks push
a `cta_click` custom event to `dataLayer` with `cta_id`/`cta_label`/`offer`
before redirecting, so GTM/GA4 can track button engagement without any
extra frontend work — just replace the placeholder `G-XXXXXXXXXX` /
`GTM-XXXXXXX` IDs with real ones and wire a Custom Event trigger on
`cta_click` in GTM.

## Backend logic summary

- `GET /click` — reads `offer` + `sub1` query params, generates a `uuid4`
  `click_id`, records `click_id, offer, sub1, timestamp, ip, user_agent` in
  a `clicks` SQLite table, then issues a `302` redirect to the matching
  brand's real website (`OFFERS` dict covers all 10 brands from the task,
  matched case-insensitively; unknown offers fall back to Zenni Optical).
- `GET /clicks` — returns all rows from `clicks`, newest first, as JSON.
- CORS is open since the frontend is a separately-hosted static site.

Tested locally end-to-end (Playwright): clicking a CTA on the running
frontend hits the backend, a row appears in `/clicks` with the correct
`offer`/`sub1`, and the browser lands on `zennioptical.com`.
