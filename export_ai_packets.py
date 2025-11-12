import sqlite3
from pathlib import Path
from collections import Counter
from app.settings import OUTPUT_DB
import tldextract

OUT = Path("data/output/ai_packets")
OUT.mkdir(parents=True, exist_ok=True)

def top_k(items, k=4):
    c = Counter([x for x in items if x])
    return [it for it, _ in c.most_common(k)]

def build_packet(domain: str, table: str, conn) -> dict:
    # Läs ut anchors och target_urls för enkel heuristik
    # Vi försöker gissa kolumnnamn robust (de kan variera något mellan kunder)
    cur = conn.cursor()
    # Hämta kolumner
    cols = [r[1] for r in cur.execute(f"PRAGMA table_info([{table}])").fetchall()]

    # Försök mappa
    def pick(col_candidates):
        for c in col_candidates:
            for real in cols:
                if real.lower() == c.lower():
                    return real
        return None

    COL_ANCHOR    = pick(["set_link_anchor","anchor","ankare"])
    COL_TARGETURL = pick(["set_link_target_url","target_url","url","målsida"])
    COL_PUBDOMAIN = pick(["pub_domain(s)","pub_domain","publisher","källa"])

    q_cols = ", ".join([c for c in [COL_ANCHOR, COL_TARGETURL, COL_PUBDOMAIN] if c])
    rows = conn.execute(f"SELECT {q_cols} FROM [{table}]").fetchall()

    anchors = []
    targets = []
    pub_domains = []
    for row in rows:
        idx = 0
        if COL_ANCHOR:    anchors.append(row[idx]); idx += 1
        if COL_TARGETURL: targets.append(row[idx]); idx += 1
        if COL_PUBDOMAIN: pub_domains.append(row[idx]); idx += 1

    # Heuristik: prioriterade sidor = topp-frekventa targets
    priority_pages = [{"url": u, "priority_score": i+1} for i, u in enumerate(top_k(targets, 6))]

    # Heuristik: vanliga ankartexter (för att guida AI:s fördelning)
    common_anchors = top_k(anchors, 8)

    packet = {
        "customer_domain": domain,
        "objective": "Planera 4 länkar som tillsammans stärker prioriterade sidor och varierar ankarprofilen.",
        "priority_pages": priority_pages,
        "history_summary": {
            "top_anchors": common_anchors,
            "top_publishers": top_k([tldextract.extract(d).registered_domain for d in pub_domains], 8),
            "total_links": len(rows),
        },
        "policy": {
            "anchor_mix": {"brand": 0.4, "exact": 0.2, "partial": 0.15, "generic": 0.2, "naked": 0.05},
            "min_variants": 3
        },
        "planned_links": [
            {"slot": 1, "needs_anchor": True, "needs_url": True},
            {"slot": 2, "needs_anchor": True, "needs_url": True},
            {"slot": 3, "needs_anchor": True, "needs_url": True},
            {"slot": 4, "needs_anchor": True, "needs_url": True},
        ]
    }
    return packet

def main():
    conn = sqlite3.connect(OUTPUT_DB)
    cur = conn.cursor()
    customers = cur.execute("SELECT domain, table_name FROM customers ORDER BY
