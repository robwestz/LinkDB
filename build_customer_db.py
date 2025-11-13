# build_customer_db.py
import sqlite3

import tldextract

SCHEMA_SQL = """
PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS customers (
  id INTEGER PRIMARY KEY,
  domain TEXT UNIQUE NOT NULL,
  brand TEXT,
  canonical_root TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS links (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
  pub_domain TEXT,
  target_domain TEXT,
  target_url TEXT,
  anchor_text TEXT,
  source_url TEXT,
  campaign TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS priority_pages (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
  url TEXT NOT NULL,
  priority_score REAL DEFAULT 0,
  intent TEXT,
  keywords TEXT
);

CREATE INDEX IF NOT EXISTS idx_links_customer ON links(customer_id);
CREATE INDEX IF NOT EXISTS idx_links_target_url ON links(target_url);
CREATE INDEX IF NOT EXISTS idx_links_target_domain ON links(target_domain);
"""


def norm_domain(val: str) -> str:
    if not isinstance(val, str) or not val.strip():
        return ""
    ext = tldextract.extract(val.strip())
    return ext.registered_domain or val.strip().lower()


def ensure_schema(con: sqlite3.Connection):
    con.executescript(SCHEMA_SQL)


def upsert_customer(
    con: sqlite3.Connection, domain: str, brand=None, canonical_root=None
) -> int:
    cur = con.execute("SELECT id FROM customers WHERE domain=?", (domain,))
    row = cur.fetchone()
    if row:
        return row[0]
    con.execute(
        "INSERT INTO customers(domain,brand,canonical_root) VALUES(?,?,?)",
        (domain, brand, canonical_root),
    )
    return con.execute("SELECT last_insert_rowid()").fetchone()[0]


def insert_link(
    con: sqlite3.Connection,
    cid: int,
    pub_domain,
    target_domain,
    target_url,
    anchor_text,
    source_url=None,
    campaign=None,
):
    con.execute(
        """INSERT INTO links(customer_id,pub_domain,target_domain,target_url,anchor_text,source_url,campaign)
                   VALUES(?,?,?,?,?,?,?)""",
        (cid, pub_domain, target_domain, target_url, anchor_text, source_url, campaign),
    )


def infer_priority_pages(con: sqlite3.Connection, cid: int, top_n: int = 6):
    cur = con.execute(
        """SELECT target_url, COUNT(*) c FROM links
                         WHERE customer_id=? GROUP BY target_url
                         ORDER BY c DESC LIMIT ?""",
        (cid, top_n),
    )
    for target_url, count in cur:
        con.execute(
            """INSERT OR IGNORE INTO priority_pages(customer_id, url, priority_score)
                       VALUES(?,?,?)""",
            (cid, target_url, float(count)),
        )
    con.commit()
