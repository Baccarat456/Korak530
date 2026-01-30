# db.py
import sqlite3
from typing import Dict, Any, List

DB_PATH = "grants.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS grants (
    id TEXT PRIMARY KEY,
    title TEXT,
    source TEXT,
    url TEXT,
    posted_date TEXT,
    deadline TEXT,
    raw JSON,
    summary TEXT,
    score REAL
);
"""

def get_conn(path: str = DB_PATH):
    conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()

def upsert_grant(grant: Dict[str, Any]):
    """
    grant must contain: id, title, source, url, posted_date, deadline, raw (json-serializable)
    """
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO grants (id, title, source, url, posted_date, deadline, raw)
    VALUES (?, ?, ?, ?, ?, ?, json(?))
    ON CONFLICT(id) DO UPDATE SET
      title=excluded.title,
      source=excluded.source,
      url=excluded.url,
      posted_date=excluded.posted_date,
      deadline=excluded.deadline,
      raw=excluded.raw;
    """, (
        grant["id"],
        grant.get("title"),
        grant.get("source"),
        grant.get("url"),
        grant.get("posted_date"),
        grant.get("deadline"),
        str(grant.get("raw", {}))
    ))
    conn.commit()
    conn.close()

def list_unscored(limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM grants WHERE score IS NULL LIMIT ?", (limit,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows

def save_summary_and_score(grant_id: str, summary: str, score: float):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("UPDATE grants SET summary = ?, score = ? WHERE id = ?", (summary, score, grant_id))
    conn.commit()
    conn.close()