from pathlib import Path

from history_repo import HistoryRepo

DB = Path(__file__).resolve().parents[1] / "data" / "output" / "linkops_history.db"

repo = HistoryRepo(DB)

# Testa med en verklig kund — funkar både med domän och full URL
for probe in [
    "https://haxan.se/",  # byt till någon du VET finns i customers
    "haxan.se",
]:
    payload = repo.build_customer_payload(probe)
    print(f"\n=== Payload for {probe} ===")
    if payload is None:
        print("Not found.")
    else:
        print("brand:", payload["brand"])
        print("canonical_root:", payload["canonical_root"])
        print("priority_pages (top):", payload["priority_pages"][:3])
        print(
            "historical_common_anchors (top):", payload["historical_common_anchors"][:5]
        )
        print("anchor mix:", payload["historical_anchor_distribution"])

repo.close()
