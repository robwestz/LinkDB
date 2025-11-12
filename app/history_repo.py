# app/history_repo.py
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Dict, Any, List, Optional
import tldextract

def _norm_domain(x: str) -> str:
    if not isinstance(x, str) or not x.strip():
        return ""
    ext = tldextract.extract(x.strip())
    reg = ext.registered_domain
    return reg or x.strip().lower()

class HistoryRepo:
    """
    Read-only repo mot linkops_history.db.
    Använd i huvudprojektet för att hämta kund-kontekst till AI-planeringen.
    """
    def __init__(self, db_path: Path):
        self.db_path = Path(db_path)
        self.con = sqlite3.connect(self.db_path)
        self.con.row_factory = sqlite3.Row

    # ------------------------
    # Kund-identifiering
    # ------------------------
    def get_customer_by_root(self, canonical_root: str) -> Optional[Dict[str, Any]]:
        row = self.con.execute(
            "SELECT id, canonical_root, brand FROM customers WHERE canonical_root = ?",
            (canonical_root.strip(),)
        ).fetchone()
        return dict(row) if row else None

    def get_customer_by_client_domain(self, client_domain_or_url: str) -> Optional[Dict[str, Any]]:
        """
        Tar emot t.ex. 'https://flaxcasino.se/' eller 'flaxcasino.se' och returnerar customers-raden.
        Matchar mot customers.canonical_root registrerad domän.
        """
        reg = _norm_domain(client_domain_or_url)
        if not reg:
            return None
        row = self.con.execute(
            "SELECT id, canonical_root, brand FROM customers"
        ).fetchall()
        for r in row:
            if _norm_domain(r["canonical_root"]) == reg:
                return dict(r)
        return None

    # ------------------------
    # Historik-sammanställning (on-the-fly)
    # ------------------------
    def priority_pages(self, customer_id: int, top_n: int = 6) -> List[Dict[str, Any]]:
        q = """
        SELECT target_url, COUNT(*) AS c
        FROM links_history
        WHERE customer_id = ?
        GROUP BY target_url
        ORDER BY c DESC
        LIMIT ?
        """
        rows = self.con.execute(q, (customer_id, top_n)).fetchall()
        return [{"url": r["target_url"], "priority_score": float(r["c"])} for r in rows]

    def common_anchors(self, customer_id: int, top_n: int = 20) -> List[Dict[str, Any]]:
        q = """
        SELECT anchor_text, COUNT(*) AS c
        FROM links_history
        WHERE customer_id = ? AND anchor_text IS NOT NULL AND TRIM(anchor_text) <> ''
        GROUP BY anchor_text
        ORDER BY c DESC
        LIMIT ?
        """
        rows = self.con.execute(q, (customer_id, top_n)).fetchall()
        return [{"anchor_text": r["anchor_text"], "count": int(r["c"])} for r in rows]

    def anchor_samples(self, customer_id: int, top_n: int = 200) -> List[Dict[str, Any]]:
        """
        Råhistorik per target_url: toppankare + frekvens. Låt AI själv avgöra exact/partial/brand/generic.
        """
        q = """
        SELECT target_url, anchor_text, COUNT(*) AS c
        FROM links_history
        WHERE customer_id = ?
          AND anchor_text IS NOT NULL AND TRIM(anchor_text) <> ''
        GROUP BY target_url, anchor_text
        ORDER BY c DESC
        LIMIT ?
        """
        rows = self.con.execute(q, (customer_id, top_n)).fetchall()
        by_url: Dict[str, List[Dict[str, Any]]] = {}
        for r in rows:
            by_url.setdefault(r["target_url"], []).append(
                {"anchor_text": r["anchor_text"], "count": int(r["c"])}
            )
        return [{"target_url": url, "anchors": anchors} for url, anchors in by_url.items()]

    def anchor_mix_guess(self, customer_id: int) -> Dict[str, float]:
        """
        Mycket enkel gissning: brand om ankartexten innehåller brandnamnet.
        Annars heuristik baserat på längd/ord – bara bra nog för AI-hintar.
        """
        brand_row = self.con.execute(
            "SELECT brand FROM customers WHERE id=?", (customer_id,)
        ).fetchone()
        brand = (brand_row["brand"] or "").lower() if brand_row else ""
        rows = self.con.execute(
            "SELECT anchor_text FROM links_history WHERE customer_id=? AND anchor_text IS NOT NULL",
            (customer_id,)
        ).fetchall()
        totals = {"brand": 0, "exact": 0, "partial": 0, "generic": 0}
        total = 0
        for r in rows:
            a = (r["anchor_text"] or "").strip()
            if not a:
                continue
            al = a.lower()
            total += 1
            if brand and brand in al:
                totals["brand"] += 1
            elif 1 <= len(a.split()) <= 2:
                totals["exact"] += 1
            elif len(a.split()) >= 3:
                totals["partial"] += 1
            else:
                totals["generic"] += 1
        if total == 0:
            return {k: 0.0 for k in totals}
        return {k: v / total for k, v in totals.items()}

    def customer_summary(self, customer_id: int) -> Dict[str, Any]:
        base = self.con.execute(
            "SELECT id, canonical_root, brand FROM customers WHERE id=?",
            (customer_id,)
        ).fetchone()
        if not base:
            return {}
        total_links = self.con.execute(
            "SELECT COUNT(*) AS c FROM links_history WHERE customer_id=?",
            (customer_id,)
        ).fetchone()["c"]
        unique_pub = self.con.execute(
            "SELECT COUNT(DISTINCT pub_domain) AS d FROM links_history WHERE customer_id=?",
            (customer_id,)
        ).fetchone()["d"]
        return {
            "customer_id": base["id"],
            "canonical_root": base["canonical_root"],
            "brand": base["brand"],
            "total_links": int(total_links),
            "unique_publication_domains": int(unique_pub),
            "priority_pages": self.priority_pages(base["id"], top_n=6),
            "historical_common_anchors": self.common_anchors(base["id"], top_n=20),
            "historical_anchor_distribution": self.anchor_mix_guess(base["id"]),
        }

    # ------------------------
    # AI-payload för en kund
    # ------------------------
    def build_customer_payload(self, client_domain_or_url: str) -> Optional[Dict[str, Any]]:
        cust = self.get_customer_by_client_domain(client_domain_or_url)
        if not cust:
            return None
        summary = self.customer_summary(cust["id"])
        return {
            "customer_domain": _norm_domain(summary["canonical_root"]),
            "brand": summary["brand"],
            "canonical_root": summary["canonical_root"],
            "priority_pages": summary["priority_pages"],                      # url + priority_score
            "historical_common_anchors": summary["historical_common_anchors"],# toppankare globalt
            "historical_anchor_samples_per_url": self.anchor_samples(summary["customer_id"], top_n=200),
            "meta": {
                "total_links": summary["total_links"],
                "unique_publication_domains": summary["unique_publication_domains"],
            },
            # Låt AI klassificera exact/partial/brand/generic självt i planeringssteget.
            "labeling_guidance": {
                "classify_anchor_types_in_ai_stage": True,
                "notes": (
                    "Jämför ankare mot titel/H1/URL/keywords på föreslagen target_url. "
                    "exact ≈ stark lexikal/semantisk överlapp; partial ≈ delvis/fraseologiskt; "
                    "brand ≈ innehåller varumärket; generic ≈ 'läs mer' etc."
                ),
            },
            # kvar som historisk hint/telemetri
            "legacy_anchor_mix_guess": summary["historical_anchor_distribution"],
        }

    def close(self):
        try:
            self.con.close()
        except Exception:
            pass
