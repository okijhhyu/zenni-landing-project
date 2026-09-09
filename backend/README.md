# Click-tracking backend

FastAPI + SQLite service used by the landing page's CTA buttons.

```
CTA (frontend) -> GET /click?offer=<brand>&sub1=<param>
    -> generates click_id
    -> stores click_id, offer, sub1, timestamp, ip, user_agent in SQLite
    -> 302 redirect to the brand's official site
```

## Endpoints

- `GET /click?offer=Zenni Optical&sub1=hero_primary`
  Records the click and 302-redirects to the brand's real site.
  `offer` is matched case-insensitively against a small lookup table
  (`OFFERS` in `main.py`) covering all 10 brands from the task list, so
  the same backend works regardless of which brand's landing page calls it.
- `GET /clicks`
  Returns every stored click as JSON, newest first.
- `GET /`
  Health check.

## Run locally

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate   # optional but recommended
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Then:

```bash
curl -i "http://127.0.0.1:8000/click?offer=Zenni%20Optical&sub1=test123"
curl "http://127.0.0.1:8000/clicks"
```

A `clicks.db` SQLite file is created automatically next to `main.py` on
first run.

## Run with Docker

```bash
cd backend
docker build -t zenni-backend .
docker run -p 8000:8000 zenni-backend
```

Or just use `docker compose up` from the project root — see the top-level
`README.md`.

## Deploy (free options)

Any Python host works. Render's free tier is the quickest:

1. Push this `backend/` folder to a GitHub repo (or the whole project repo).
2. On [render.com](https://render.com) → **New Web Service** → connect the repo.
   - Root directory: `backend`
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     (a `Procfile` with the same command is included, so Render/Heroku-style
     platforms can also auto-detect it)
3. Deploy. Render gives you a public URL like `https://your-app.onrender.com`.
4. Put that URL in the frontend's `VITE_BACKEND_URL` env var (see
   `frontend/.env.example`) and rebuild the frontend.

Railway, Fly.io, or PythonAnywhere work the same way — install
`requirements.txt`, run the uvicorn start command, expose the port.
Render, Railway and Fly.io can also all deploy straight from the included
`Dockerfile` instead of buildpacks, if you prefer.

## Notes on the implementation

- `click_id` is a `uuid4`, stored as the primary key.
- SQLite is used for zero-setup persistence; `clicks` table has one row per
  click with `click_id, offer, sub1, timestamp, ip, user_agent`.
- CORS is open (`allow_origins=["*"]`) since the frontend is a static site
  deployed on a different origin and only GET/no-cookie endpoints are exposed.
- `ip` prefers `X-Forwarded-For` (set by most PaaS reverse proxies) and falls
  back to the raw connection IP for local runs.
