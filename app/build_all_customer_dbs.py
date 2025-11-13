# app/build_all_customer_dbs.py
from __future__ import annotations

import re
import sqlite3
from pathlib import Path

from rich import print

ROOT = Path(__file__).resolve().parents[1]
SRC_DB = ROOT / "data" / "output" / "linkops_history.db"
OUT_DIR = ROOT / "data" / "output" / "customers"

SCHEMA_SQL = """
PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS customers (
  id INTEGER PRIMARY KEY,
  canonical_root TEXT UNIQUE NOT NULL,
  brand TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS links_history (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
  pub_page_url TEXT NOT NULL,
  pub_domain TEXT,
  target_url TEXT NOT NULL,
  target_domain TEXT,
  anchor_text TEXT,
  link_type TEXT,
  language TEXT,
  published_at TEXT,
  topic_tags TEXT,
  context_excerpt TEXT,
  anchor_type TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS priority_pages (
  id INTEGER PRIMARY KEY,
  url TEXT NOT NULL,
  priority_score REAL DEFAULT 0,
  intent TEXT,
  keywords TEXT
);

CREATE VIEW IF NOT EXISTS v_summary AS
SELECT
  c.canonical_root AS customer,
  c.brand AS brand,
  (SELECT COUNT(*) FROM links_history lh) AS total_links,
  (SELECT COUNT(DISTINCT lh.pub_domain) FROM links_history lh) AS unique_pub_domains
FROM customers c
LIMIT 1;
"""


def ensure_schema(con: sqlite3.Connection):
    con.executescript(SCHEMA_SQL)


def safe_dir_token(canonical_root: str | None, brand: str | None, cid: int) -> str:
    """
    Gör ett säkert katalognamn:
    - Ta i första hand registrerad domänliknande sträng ur canonical_root
    - Annars brand
    - Annars cust_<id>
    - Endast [a-z0-9.-], allt annat -> "_"
    """
    candidate = (canonical_root or "").strip() or (brand or "").strip()
    candidate = candidate.replace("http://", "").replace("https://", "")
    candidate = candidate.replace("/", "_").strip().lower()

    # tillåt bara säkra tecken
    candidate = re.sub(r"[^a-z0-9\.\-]", "_", candidate)
    # trimma överflödiga underscores & punkter i kanter
    candidate = candidate.strip("._-")
    if not candidate:
        candidate = f"cust_{cid}"
    return candidate


def build_one_customer_db(
    src_con: sqlite3.Connection,
    customer_id: int,
    canonical_root: str,
    brand: str | None,
) -> Path:
    # hämta kundens rad
    c_row = src_con.execute(
        "SELECT id, canonical_root, brand, created_at FROM customers WHERE id=?",
        (customer_id,),
    ).fetchone()
    # hämta kundens historik
    links = src_con.execute(
        "SELECT * FROM links_history WHERE customer_id=?", (customer_id,)
    ).fetchall()

    # skapa målfil (säker katalognamn)
    safe = safe_dir_token(canonical_root, brand, customer_id)
    dst_dir = OUT_DIR / safe
    dst_dir.mkdir(parents=True, exist_ok=True)
    dst_db = dst_dir / "customer.db"

    dst_con = sqlite3.connect(dst_db)
    dst_con.row_factory = sqlite3.Row
    ensure_schema(dst_con)

    # skriv customers
    dst_con.execute(
        "INSERT OR REPLACE INTO customers(id, canonical_root, brand, created_at) VALUES(?,?,?,?)",
        (c_row["id"], c_row["canonical_root"], c_row["brand"], c_row["created_at"]),
    )

    # skriv links_history (kolumn-intersection källa ↔ mål)
    if links:
        src_cols_rows = src_con.execute("PRAGMA table_info(links_history)").fetchall()
        src_cols = [
            r["name"] if isinstance(r, sqlite3.Row) else r[1] for r in src_cols_rows
        ]

        dst_cols_rows = dst_con.execute("PRAGMA table_info(links_history)").fetchall()
        dst_cols = [
            r["name"] if isinstance(r, sqlite3.Row) else r[1] for r in dst_cols_rows
        ]

        cols = [c for c in src_cols if c in dst_cols]
        insert_cols = ",".join(cols)
        placeholders = ",".join(["?"] * len(cols))

        for r in links:
            dst_con.execute(
                f"INSERT INTO links_history({insert_cols}) VALUES({placeholders})",
                tuple(r[c] for c in cols),
            )

    # priority_pages (enkel heuristik: flest länkar per target_url)
    pp_rows = dst_con.execute(
        """
        SELECT target_url, COUNT(*) AS c
        FROM links_history
        GROUP BY target_url
        ORDER BY c DESC
        LIMIT 12
    """
    ).fetchall()
    for r in pp_rows:
        dst_con.execute(
            "INSERT INTO priority_pages(url, priority_score) VALUES(?,?)",
            (r["target_url"], float(r["c"])),
        )

    dst_con.commit()
    dst_con.close()
    return dst_db


def main():
    if not SRC_DB.exists():
        raise FileNotFoundError(f"Saknar källdatabas: {SRC_DB}")
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    src = sqlite3.connect(SRC_DB)
    src.row_factory = sqlite3.Row

    customers = src.execute(
        "SELECT id, canonical_root, brand FROM customers ORDER BY canonical_root"
    ).fetchall()
    print(f"[cyan]Hittade {len(customers)} kunder – bygger per-kund-databaser...[/]")

    built = 0
    failures = 0
    for row in customers:
        try:
            db_path = build_one_customer_db(
                src, row["id"], row["canonical_root"], row["brand"]
            )
            built += 1
            print(f"[green]✔[/] {row['canonical_root']} → {db_path.relative_to(ROOT)}")
        except Exception as e:
            failures += 1
            print(f"[red]✖[/] {row['canonical_root']!r} misslyckades: {e}")

    src.close()
    print(
        f"[bold green]\nKlar![/] {built} kunddatabaser skapade under {OUT_DIR.relative_to(ROOT)}"
    )
    if failures:
        print(
            f"[yellow]Obs:[/] {failures} kunder hoppades över p.g.a. fel. Se loggen ovan."
        )


if __name__ == "__main__":
    main()
