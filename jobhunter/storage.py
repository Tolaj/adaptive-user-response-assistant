# jobhunter/storage.py
# ─────────────────────────────────────────────────────────────────────────────
# SQLite for deduplication + CSV for your readable output.
# Every job gets a unique ID (hash of title+company+site).
# If the same job is found again, it's silently skipped.
# ─────────────────────────────────────────────────────────────────────────────

import csv
import hashlib
import sqlite3
from datetime import datetime
from pathlib import Path

from jobhunter.config import DB_PATH, CSV_PATH


# ── Schema ─────────────────────────────────────────────────────────────────
_CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS jobs (
    id          TEXT PRIMARY KEY,
    title       TEXT,
    company     TEXT,
    location    TEXT,
    salary      TEXT,
    posted      TEXT,
    url         TEXT,
    snippet     TEXT,
    site        TEXT,
    score       INTEGER,
    score_reason TEXT,
    found_at    TEXT
);
"""

_CSV_HEADERS = [
    "found_at", "site", "score", "title", "company",
    "location", "salary", "posted", "url", "snippet", "score_reason"
]


def _get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute(_CREATE_TABLE)
    conn.commit()
    return conn


def _job_id(title: str, company: str, site: str) -> str:
    """Stable hash — same job from same site always gets same ID."""
    raw = f"{title.lower().strip()}|{company.lower().strip()}|{site.lower()}"
    return hashlib.md5(raw.encode()).hexdigest()


def is_seen(title: str, company: str, site: str) -> bool:
    """Return True if this job is already in the database."""
    job_id = _job_id(title, company, site)
    conn = _get_conn()
    row = conn.execute("SELECT 1 FROM jobs WHERE id=?", (job_id,)).fetchone()
    conn.close()
    return row is not None


def save_job(job: dict, site: str, score: int, score_reason: str) -> bool:
    """
    Save a job to SQLite + append to CSV.
    Returns True if saved (new), False if duplicate (skipped).
    """
    title   = job.get("title", "Unknown")
    company = job.get("company", "Unknown")

    if is_seen(title, company, site):
        return False  # already have this one

    job_id   = _job_id(title, company, site)
    found_at = datetime.now().strftime("%Y-%m-%d %H:%M")

    row = {
        "id":           job_id,
        "title":        title,
        "company":      company,
        "location":     job.get("location", ""),
        "salary":       job.get("salary", ""),
        "posted":       job.get("posted", ""),
        "url":          job.get("url", ""),
        "snippet":      job.get("snippet", ""),
        "site":         site,
        "score":        score,
        "score_reason": score_reason,
        "found_at":     found_at,
    }

    # ── Write to SQLite ──────────────────────────────────────────────────
    conn = _get_conn()
    conn.execute(
        """INSERT OR IGNORE INTO jobs
           (id,title,company,location,salary,posted,url,snippet,site,score,score_reason,found_at)
           VALUES (:id,:title,:company,:location,:salary,:posted,:url,:snippet,:site,:score,:score_reason,:found_at)""",
        row,
    )
    conn.commit()
    conn.close()

    # ── Append to CSV ────────────────────────────────────────────────────
    csv_exists = CSV_PATH.exists()
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=_CSV_HEADERS)
        if not csv_exists:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in _CSV_HEADERS})

    return True


def get_stats() -> dict:
    """Return summary stats for logging."""
    conn = _get_conn()
    total = conn.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    today = conn.execute(
        "SELECT COUNT(*) FROM jobs WHERE found_at >= date('now')"
    ).fetchone()[0]
    top = conn.execute(
        "SELECT title, company, score FROM jobs ORDER BY score DESC LIMIT 3"
    ).fetchall()
    conn.close()
    return {"total": total, "today": today, "top_3": top}