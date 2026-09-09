"""
Click-tracking backend for the landing page test task.

Flow:
    CTA (frontend) -> GET /click?offer=<brand>&sub1=<param>
        -> generates click_id
        -> stores click_id, offer, sub1, timestamp, ip, user_agent in SQLite
        -> 302 redirect to the brand's official website
    GET /clicks    -> JSON dump of all stored clicks
    GET /dashboard -> human-friendly HTML view of all stored clicks
"""

import sqlite3
import uuid
from collections import Counter
from contextlib import contextmanager
from datetime import datetime, timezone
from html import escape
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse

DB_PATH = Path(__file__).parent / "clicks.db"

# Official destination URL for every brand in the test-task list.
# "offer" is matched case-insensitively so ?offer=Zenni%20Optical or
# ?offer=zenni-optical both resolve correctly.
OFFERS = {
    "dell": "https://www.dell.com",
    "macys": "https://www.macys.com",
    "macy's": "https://www.macys.com",
    "office depot": "https://www.officedepot.com",
    "keiser university": "https://www.keiseruniversity.edu",
    "choice hotels": "https://www.choicehotels.com",
    "vivid seats": "https://www.vividseats.com",
    "zenni optical": "https://www.zennioptical.com",
    "houzz": "https://www.houzz.com",
    "ziprecruiter": "https://www.ziprecruiter.com",
    "state farm": "https://www.statefarm.com",
}

# The brand this particular landing page was built for. Used as a fallback
# if an unrecognised offer value is supplied.
DEFAULT_OFFER = "zenni optical"

app = FastAPI(title="Click Tracker")

# Wide-open CORS: the frontend is a static site hosted on a different
# origin (Vercel/Netlify/GitHub Pages/etc). Only GET endpoints are exposed
# and nothing sensitive is returned, so this is safe for this test task.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with get_db() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS clicks (
                click_id   TEXT PRIMARY KEY,
                offer      TEXT NOT NULL,
                sub1       TEXT,
                timestamp  TEXT NOT NULL,
                ip         TEXT,
                user_agent TEXT
            )
            """
        )


init_db()


def resolve_redirect_url(offer: str) -> str:
    """Look up the destination URL for an offer, case-insensitively."""
    if not offer:
        return OFFERS[DEFAULT_OFFER]
    return OFFERS.get(offer.strip().lower(), OFFERS[DEFAULT_OFFER])


def client_ip(request: Request) -> str:
    # Respect a reverse-proxy header (Render/Railway/etc put the real
    # client IP here) and fall back to the direct connection IP.
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else ""


@app.get("/click")
def click(offer: str = "", sub1: str = "", request: Request = None):
    click_id = str(uuid.uuid4())
    timestamp = datetime.now(timezone.utc).isoformat()
    ip = client_ip(request)
    user_agent = request.headers.get("user-agent", "")

    with get_db() as conn:
        conn.execute(
            """
            INSERT INTO clicks (click_id, offer, sub1, timestamp, ip, user_agent)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (click_id, offer, sub1, timestamp, ip, user_agent),
        )

    destination = resolve_redirect_url(offer)
    return RedirectResponse(url=destination, status_code=302)


@app.get("/clicks")
def clicks():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT click_id, offer, sub1, timestamp, ip, user_agent "
            "FROM clicks ORDER BY timestamp DESC"
        ).fetchall()
    return JSONResponse([dict(row) for row in rows])


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT click_id, offer, sub1, timestamp, ip, user_agent "
            "FROM clicks ORDER BY timestamp DESC"
        ).fetchall()

    total = len(rows)
    by_offer = Counter(r["offer"] or "—" for r in rows)
    by_sub1 = Counter(r["sub1"] or "—" for r in rows)
    top_offer = by_offer.most_common(1)[0] if by_offer else ("—", 0)
    top_sub1 = by_sub1.most_common(1)[0] if by_sub1 else ("—", 0)

    def stat_card(label: str, value: str) -> str:
        return f"""
        <div class="card">
          <div class="card-label">{escape(label)}</div>
          <div class="card-value">{escape(str(value))}</div>
        </div>"""

    stats_html = "".join([
        stat_card("Total clicks", total),
        stat_card("Top offer", f"{top_offer[0]} ({top_offer[1]})"),
        stat_card("Top CTA (sub1)", f"{top_sub1[0]} ({top_sub1[1]})"),
    ])

    def fmt_ts(ts: str) -> str:
        try:
            dt = datetime.fromisoformat(ts)
            return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
        except ValueError:
            return ts

    if rows:
        rows_html = "".join(
            f"""
            <tr>
              <td class="mono">{escape(fmt_ts(r['timestamp']))}</td>
              <td><span class="badge">{escape(r['offer'] or '—')}</span></td>
              <td>{escape(r['sub1'] or '—')}</td>
              <td class="mono dim">{escape(r['ip'] or '—')}</td>
              <td class="dim ua">{escape(r['user_agent'] or '—')}</td>
              <td class="mono dim small">{escape(r['click_id'])}</td>
            </tr>"""
            for r in rows
        )
    else:
        rows_html = """
            <tr><td colspan="6" class="empty">No clicks recorded yet.</td></tr>"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta http-equiv="refresh" content="15">
<title>Click Tracker — Dashboard</title>
<style>
  :root {{
    --bg: #0f1115;
    --panel: #171a21;
    --border: #262b36;
    --text: #e8eaed;
    --dim: #8b93a1;
    --accent: #6ea8fe;
    --accent-bg: rgba(110, 168, 254, 0.12);
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 40px 24px 64px;
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  }}
  .wrap {{ max-width: 1080px; margin: 0 auto; }}
  h1 {{ font-size: 22px; font-weight: 600; margin: 0 0 4px; }}
  .subtitle {{ color: var(--dim); font-size: 14px; margin: 0 0 28px; }}
  .cards {{ display: flex; gap: 16px; margin-bottom: 28px; flex-wrap: wrap; }}
  .card {{
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px 20px;
    min-width: 180px;
    flex: 1;
  }}
  .card-label {{ color: var(--dim); font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; margin-bottom: 6px; }}
  .card-value {{ font-size: 20px; font-weight: 600; }}
  table {{
    width: 100%;
    border-collapse: collapse;
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 12px;
    overflow: hidden;
    font-size: 13px;
  }}
  thead th {{
    text-align: left;
    padding: 12px 14px;
    background: #1c2028;
    color: var(--dim);
    font-weight: 600;
    text-transform: uppercase;
    font-size: 11px;
    letter-spacing: 0.04em;
    border-bottom: 1px solid var(--border);
  }}
  tbody td {{
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
    vertical-align: top;
  }}
  tbody tr:last-child td {{ border-bottom: none; }}
  tbody tr:hover {{ background: #1a1e26; }}
  .mono {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; }}
  .dim {{ color: var(--dim); }}
  .small {{ font-size: 11px; }}
  .ua {{ max-width: 260px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .badge {{
    display: inline-block;
    background: var(--accent-bg);
    color: var(--accent);
    padding: 2px 9px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
  }}
  .empty {{ text-align: center; color: var(--dim); padding: 32px; }}
  .footer {{ margin-top: 16px; color: var(--dim); font-size: 12px; }}
  a {{ color: var(--accent); }}
</style>
</head>
<body>
  <div class="wrap">
    <h1>Click Tracker</h1>
    <p class="subtitle">Auto-refreshes every 15s · raw JSON at <a href="/clicks">/clicks</a></p>
    <div class="cards">{stats_html}</div>
    <table>
      <thead>
        <tr>
          <th>Time</th>
          <th>Offer</th>
          <th>Sub1 (CTA)</th>
          <th>IP</th>
          <th>User agent</th>
          <th>Click ID</th>
        </tr>
      </thead>
      <tbody>{rows_html}
      </tbody>
    </table>
    <p class="footer">{total} click(s) total.</p>
  </div>
</body>
</html>"""
    return HTMLResponse(content=html)


@app.get("/")
def health():
    return {"status": "ok", "service": "click-tracker"}
