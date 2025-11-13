"""
Complete November Plan - Sätter målsidor och ankartexter för alla länkar
"""

import re
import sqlite3
from pathlib import Path

import pandas as pd

# Paths
base_dir = Path(__file__).parent
csv_path = base_dir / "november_plan.csv"
db_path = base_dir / "data" / "output" / "linkops_history.db"
output_path = base_dir / "november_plan_completed.csv"

# Läs CSV
df = pd.read_csv(csv_path)
print(f"Totalt rader: {len(df)}")

# Anslut till databas
con = sqlite3.connect(db_path)
con.row_factory = sqlite3.Row

# Spara original för jämförelse
original_needs_target = df["target_url"].isna().sum()
original_needs_anchor = df["link_anchor"].isna().sum()

print(f"Behöver målsida: {original_needs_target}")
print(f"Behöver ankartext: {original_needs_anchor}")
print("\n" + "=" * 70)
print("KOMPLETTERAR LÄNKAR...")
print("=" * 70 + "\n")

completed = 0

for idx, row in df.iterrows():
    kund = str(row.get("kund_brand", "")).strip()
    pub_domain = str(row.get("publication_domain", "")).strip()
    market = str(row.get("market", "SE")).strip()
    target_url = row.get("target_url")
    anchor = row.get("link_anchor")

    # Skippa tomma rader
    if pd.isna(kund) or kund == "" or kund == "nan":
        continue

    needs_target = pd.isna(target_url) or target_url == ""
    needs_anchor = pd.isna(anchor) or anchor == ""

    if not needs_target and not needs_anchor:
        continue  # Redan komplett

    # Hitta kund i databas
    customer = con.execute(
        "SELECT id, canonical_root, brand FROM customers WHERE canonical_root LIKE ? OR brand LIKE ?",
        (f"%{kund}%", f"%{kund}%"),
    ).fetchone()

    if not customer:
        print(
            f"⚠️  Rad {idx}: Kund '{kund}' ej funnen i databas - använder generisk data"
        )

        # Generisk komplettering för okända kunder
        if needs_target:
            # Gissa domän från kundnamn
            domain_guess = kund.lower().replace(" ", "").replace("&", "")
            if not domain_guess.endswith(".com") and not domain_guess.endswith(".se"):
                domain_guess += ".com"
            df.at[idx, "target_url"] = f"https://{domain_guess}"

        if needs_anchor:
            # Branded anchor
            df.at[idx, "link_anchor"] = kund

        completed += 1
        continue

    customer_id = customer["id"]
    canonical_root = customer["canonical_root"]

    # Hämta historiska målsidor
    if needs_target:
        common_targets = con.execute(
            """
            SELECT target_url, COUNT(*) as cnt
            FROM links_history
            WHERE customer_id = ? AND target_url IS NOT NULL AND target_url != ''
            GROUP BY target_url
            ORDER BY cnt DESC
            LIMIT 5
        """,
            (customer_id,),
        ).fetchall()

        if common_targets:
            # Använd vanligaste målsidan
            df.at[idx, "target_url"] = common_targets[0]["target_url"]
            print(f"✓ Rad {idx}: {kund} → målsida: {common_targets[0]['target_url']}")
        else:
            # Fallback: använd canonical_root
            df.at[idx, "target_url"] = f"https://{canonical_root}"
            print(f"✓ Rad {idx}: {kund} → målsida (fallback): https://{canonical_root}")

    # Hämta historiska ankartexter
    if needs_anchor:
        common_anchors = con.execute(
            """
            SELECT anchor_text, COUNT(*) as cnt
            FROM links_history
            WHERE customer_id = ? AND anchor_text IS NOT NULL AND anchor_text != ''
            GROUP BY anchor_text
            ORDER BY cnt DESC
            LIMIT 20
        """,
            (customer_id,),
        ).fetchall()

        if common_anchors:
            # Välj en varierad ankartext baserat på radnummer för att undvika upprepningar
            anchor_idx = idx % len(common_anchors)
            selected_anchor = common_anchors[anchor_idx]["anchor_text"]
            df.at[idx, "link_anchor"] = selected_anchor
            print(f"✓ Rad {idx}: {kund} → ankar: '{selected_anchor}'")
        else:
            # Fallback: använd brand
            df.at[idx, "link_anchor"] = customer["brand"] or kund
            print(
                f"✓ Rad {idx}: {kund} → ankar (fallback): '{customer['brand'] or kund}'"
            )

    completed += 1

con.close()

# Spara komplett CSV
df.to_csv(output_path, index=False)

print("\n" + "=" * 70)
print("RESULTAT")
print("=" * 70)
print(f"Kompletterade länkar: {completed}")
print(f"Ursprungligen saknade målsidor: {original_needs_target}")
print(f"Ursprungligen saknade ankartexter: {original_needs_anchor}")
print(f"\nKomplett plan sparad: {output_path}")
print("\n✅ KLART! November-planeringen är nu komplett!")
