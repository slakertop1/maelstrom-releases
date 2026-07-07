"""Лендинг + приём лидов: FastAPI отдаёт статику и принимает POST /api/lead.

Каждый лид сохраняется в SQLite и мгновенно улетает в Telegram владельцу.
"""

import logging
import os
import time
from collections import deque
from pathlib import Path

import aiosqlite
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN", "").strip()
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", "").strip()
DB_PATH = os.environ.get("DB_PATH", "data/leads.db")

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

SCHEMA = """
CREATE TABLE IF NOT EXISTS leads (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    name       TEXT NOT NULL,
    contact    TEXT NOT NULL,
    message    TEXT,
    ip         TEXT,
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

app = FastAPI(title="Lead landing", docs_url=None, redoc_url=None)


class Lead(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    contact: str = Field(min_length=5, max_length=100)  # телефон или @telegram
    message: str = Field(default="", max_length=1000)
    website: str = Field(default="")  # honeypot: люди это поле не видят и не заполняют


# Простейший rate limit: не больше 5 заявок с одного IP за 10 минут.
_recent: dict[str, deque[float]] = {}


def _rate_limited(ip: str, limit: int = 5, window: float = 600.0) -> bool:
    now = time.monotonic()
    bucket = _recent.setdefault(ip, deque())
    while bucket and now - bucket[0] > window:
        bucket.popleft()
    if len(bucket) >= limit:
        return True
    bucket.append(now)
    return False


async def _notify_telegram(lead: Lead) -> None:
    if not BOT_TOKEN or not ADMIN_CHAT_ID:
        logger.warning("BOT_TOKEN/ADMIN_CHAT_ID не заданы — уведомление не отправлено")
        return
    text = (
        "🔔 Новая заявка с сайта\n"
        f"Имя: {lead.name}\n"
        f"Контакт: {lead.contact}\n"
        f"Сообщение: {lead.message or '—'}"
    )
    async with httpx.AsyncClient(timeout=10) as client:
        resp = await client.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": ADMIN_CHAT_ID, "text": text},
        )
        if resp.status_code != 200:
            logger.error("Telegram API вернул %s: %s", resp.status_code, resp.text)


@app.on_event("startup")
async def startup() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
    Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()


@app.post("/api/lead")
async def create_lead(lead: Lead, request: Request) -> JSONResponse:
    if lead.website:  # honeypot сработал — это бот, тихо "принимаем" и выбрасываем
        return JSONResponse({"ok": True})

    ip = request.client.host if request.client else "unknown"
    if _rate_limited(ip):
        return JSONResponse({"ok": False, "error": "Слишком много заявок, попробуйте позже"}, 429)

    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO leads (name, contact, message, ip) VALUES (?, ?, ?, ?)",
            (lead.name.strip(), lead.contact.strip(), lead.message.strip(), ip),
        )
        await db.commit()

    try:
        await _notify_telegram(lead)
    except Exception:  # сбой уведомления не должен ронять приём лида — он уже в базе
        logger.exception("Не удалось отправить уведомление в Telegram")

    return JSONResponse({"ok": True})


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


app.mount("/", StaticFiles(directory=STATIC_DIR), name="static")
