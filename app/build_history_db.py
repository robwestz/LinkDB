# app/build_history_db.py
import sqlite3
from pathlib import Path

import pandas as pd
import tldextract
from rich import print
from settings import COLUMNS, DB_PATH, INPUT_XLSX, OPTIONAL

SCHEMA_FILE = Path(__file__).parent / "schema.sql"


def norm_domain(url: str) -> str:
    """
    Tar ut registrerad domän från URL eller domänsträng.
    Faller tillbaka till lowercased url om tldextract inte hittar suffix.
    """
    if not isinstance(url, str) or not url.strip():
        return ""
    url = url.strip()
    ext = tldextract.extract(url)
    # ext.registered_domain kan vara tom om strängen är konstig (typ "www.x")
    reg = ext.registered_domain
    return reg.lower() if reg else url.lower()


def ensure_schema(con: sqlite3.Connection):
    schema = SCHEMA_FILE.read_text(encoding="utf-8")
    con.executescript(schema)
    # Lite robustare default
    con.execute("PRAGMA foreign_keys = ON;")
    con.execute("PRAGMA journal_mode = WAL;")


def upsert_customer(con: sqlite3.Connection, canonical_root: str, brand: str | None):
    cur = con.execute(
        "SELECT id FROM customers WHERE canonical_root = ?", (canonical_root,)
    )
    row = cur.fetchone()
    if row:
        return row[0]
    con.execute(
        "INSERT INTO customers (canonical_root, brand) VALUES (?, ?)",
        (canonical_root, brand),
    )
    return con.execute("SELECT last_insert_rowid()").fetchone()[0]


def main():
    print(f"[cyan]📥 Läser Excel:[/] {INPUT_XLSX}")
    if not INPUT_XLSX.exists():
        raise FileNotFoundError(f"Filen {INPUT_XLSX} saknas")

    # openpyxl för .xlsx
    df = pd.read_excel(INPUT_XLSX, engine="openpyxl")
    print(f"[green]✅ Läst {len(df)} rader från Excel[/]")

    # Kontrollera obligatoriska kolumner
    missing = [v for v in COLUMNS.values() if v not in df.columns]
    if missing:
        raise ValueError(f"Saknade kolumner i Excel: {missing}")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(DB_PATH)
    ensure_schema(con)

    inserted_links = 0
    customers_created = 0
    customer_cache: dict[str, int] = {}

    # Kör i en transaktion för hastighet
    with con:
        for _, row in df.iterrows():
            canonical_root = str(row[COLUMNS["canonical_root"]] or "").strip()
            if not canonical_root:
                continue
            brand = (
                str(row[COLUMNS["brand"]]).strip()
                if COLUMNS["brand"] in df.columns
                else None
            )

            # Upsert kund (cachear id lokalt)
            cid = customer_cache.get(canonical_root)
            if cid is None:
                cid = upsert_customer(con, canonical_root, brand)
                customer_cache[canonical_root] = cid
                customers_created += 1

            # --- normalisering av nyckelfält (matchar UNIQUE-indexet) ---
            pub_page_url = str(row[COLUMNS["pub_page_url"]] or "").strip()
            target_url = str(row[COLUMNS["target_url"]] or "").strip()
            anchor_text = str(row[COLUMNS["anchor_text"]] or "").strip()
            published_at = str(
                row[COLUMNS["published_at"]] or ""
            ).strip()  # '' istället för NULL

            if not pub_page_url or not target_url:
                continue  # kräver båda för en giltig rad

            data = {
                "customer_id": cid,
                "pub_page_url": pub_page_url,
                "pub_domain": norm_domain(pub_page_url),
                "target_url": target_url,
                "target_domain": norm_domain(target_url),
                "anchor_text": anchor_text,
                "link_type": str(row[COLUMNS["link_type"]] or "").strip(),
                "language": str(row[COLUMNS["language"]] or "").strip(),
                "published_at": published_at,  # viktigt: aldrig NULL, matchar UNIQUE-index
            }

            # Lägg till frivilliga fält om de finns
            for col in OPTIONAL:
                if col in df.columns:
                    data[col] = str(row[col] or "").strip()

            # Idempotent insert – undviker dubletter vid upprepad import
            placeholders = ", ".join(["?"] * len(data))
            columns = ", ".join(data.keys())
            con.execute(
                f"INSERT OR IGNORE INTO links_history ({columns}) VALUES ({placeholders})",
                tuple(data.values()),
            )
            inserted_links += 1

    con.close()

    print(f"[bold green]✅ Import klar![/]")
    print(f"📊 {inserted_links} rader processade (dubletter ignoreras tyst)")
    print(f"👥 {customers_created} kunder upsertade")
    print(f"💾 Databas: {DB_PATH}")


if __name__ == "__main__":
    main()
