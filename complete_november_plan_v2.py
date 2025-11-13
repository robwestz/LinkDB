"""
Complete November Plan v2 - Med manuell kontext för okända kunder
"""

import sqlite3
from pathlib import Path

import pandas as pd

# Manuell mappning för kunder som inte finns i databasen
MANUAL_CUSTOMER_DATA = {
    "Vera&John": {
        "domain": "verajohn.com",
        "target_urls": [
            "https://www.verajohn.com/sv",
            "https://www.verajohn.com/sv/casino",
            "https://www.verajohn.com/sv/live-casino",
        ],
        "anchors": [
            "Vera&John",
            "Vera&John casino",
            "casino online",
            "spela casino",
            "casinospel",
        ],
    },
    "Lucky Casino": {
        "domain": "luckycasino.com",
        "target_urls": [
            "https://luckycasino.com/sv/",
            "https://luckycasino.com/sv/casino",
        ],
        "anchors": ["Lucky Casino", "casino bonus", "online casino", "spela casino"],
    },
    "Fair Investments": {
        "domain": "fairinvestments.se",
        "target_urls": [
            "https://fairinvestments.se",
            "https://www.linkedin.com/company/fair-investments-sweden-ab",
        ],
        "anchors": [
            "Fair Investments",
            "investering",
            "kapitalförvaltning",
            "finansiella tjänster",
            "investeringsbolag",
        ],
    },
    "Zmarta Sverige": {
        "domain": "zmarta.se",
        "target_urls": [
            "https://www.zmarta.se/",
            "https://www.zmarta.se/lana-pengar",
            "https://www.zmarta.se/lana-pengar/privatlan",
        ],
        "anchors": [
            "Zmarta",
            "jämför lån",
            "privatlån",
            "låna pengar",
            "lånekalkylator",
            "bästa lånen",
        ],
    },
    "Florister I Sverige": {
        "domain": "florister.se",
        "target_urls": ["https://florister.se", "https://florister.se/blomsterbutiker"],
        "anchors": [
            "Florister i Sverige",
            "blomsterbutik",
            "beställ blommor",
            "blomsterleverans",
        ],
    },
    "D-Bet": {
        "domain": "dbet.com",
        "target_urls": [
            "https://www.dbet.com/",
            "https://www.dbet.com/sports/",
            "https://www.dbet.com/sportnyheter-och-sponsorskap/3/dbet-huvudsponsor-handbollsligan-2025/",
        ],
        "anchors": ["D-Bet", "betting online", "sportbetting", "odds", "livebetting"],
    },
    "Nordic Knots": {
        "domain": "nordicknots.com",
        "target_urls": [
            "https://www.nordicknots.com/us/rugs",
            "https://www.nordicknots.com/us/custom-rugs",
        ],
        "anchors": [
            "Nordic Knots",
            "handmade rugs",
            "custom rugs",
            "scandinavian rugs",
        ],
    },
    "Epidemic Sound": {
        "domain": "epidemicsound.com",
        "target_urls": [
            "https://www.epidemicsound.com/music/",
            "https://www.epidemicsound.com/es/music",
        ],
        "anchors": [
            "Epidemic Sound",
            "royalty-free music",
            "music library",
            "background music",
            "stock music",
        ],
    },
}

# Paths
base_dir = Path(__file__).parent
csv_path = base_dir / "november_plan.csv"
db_path = base_dir / "data" / "output" / "linkops_history.db"
output_path = base_dir / "november_plan_completed.csv"

# Läs CSV
df = pd.read_csv(csv_path)
print(f"📋 Totalt rader: {len(df)}")

# Anslut till databas
con = sqlite3.connect(db_path)
con.row_factory = sqlite3.Row

# Statistik
original_needs_target = df["target_url"].isna().sum()
original_needs_anchor = df["link_anchor"].isna().sum()

print(f"❌ Saknar målsida: {original_needs_target}")
print(f"❌ Saknar ankartext: {original_needs_anchor}")
print("\n" + "=" * 70)
print("🤖 KOMPLETTERAR NOVEMBER-PLANERINGEN...")
print("=" * 70 + "\n")

completed_targets = 0
completed_anchors = 0

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
        continue

    # Kolla om kunden finns i manuell mappning
    if kund in MANUAL_CUSTOMER_DATA:
        manual_data = MANUAL_CUSTOMER_DATA[kund]

        if needs_target:
            # Använd första målsidan (kan rotera senare om behövs)
            target_idx = idx % len(manual_data["target_urls"])
            df.at[idx, "target_url"] = manual_data["target_urls"][target_idx]
            print(
                f"✓ Rad {idx}: {kund} → målsida: {manual_data['target_urls'][target_idx]} (manuell)"
            )
            completed_targets += 1

        if needs_anchor:
            # Rotera genom ankartexter
            anchor_idx = idx % len(manual_data["anchors"])
            df.at[idx, "link_anchor"] = manual_data["anchors"][anchor_idx]
            print(
                f"✓ Rad {idx}: {kund} → ankar: '{manual_data['anchors'][anchor_idx]}' (manuell)"
            )
            completed_anchors += 1

        continue

    # Annars, hitta i databas
    customer = con.execute(
        "SELECT id, canonical_root, brand FROM customers WHERE canonical_root LIKE ? OR brand LIKE ?",
        (f"%{kund}%", f"%{kund}%"),
    ).fetchone()

    if not customer:
        print(
            f"⚠️  Rad {idx}: Kund '{kund}' varken i databas eller manuell mappning - använder generisk"
        )

        if needs_target:
            domain_guess = kund.lower().replace(" ", "").replace("&", "")
            if not any(
                domain_guess.endswith(ext) for ext in [".com", ".se", ".io", ".ai"]
            ):
                domain_guess += ".com"
            df.at[idx, "target_url"] = f"https://{domain_guess}"
            completed_targets += 1

        if needs_anchor:
            df.at[idx, "link_anchor"] = kund
            completed_anchors += 1

        continue

    customer_id = customer["id"]
    canonical_root = customer["canonical_root"]

    # Hämta från databas
    if needs_target:
        common_targets = con.execute(
            """
            SELECT target_url, COUNT(*) as cnt
            FROM links_history
            WHERE customer_id = ? AND target_url IS NOT NULL AND target_url != ''
            GROUP BY target_url
            ORDER BY cnt DESC
            LIMIT 10
        """,
            (customer_id,),
        ).fetchall()

        if common_targets:
            # Rotera genom top-målsidor
            target_idx = idx % len(common_targets)
            df.at[idx, "target_url"] = common_targets[target_idx]["target_url"]
            print(
                f"✓ Rad {idx}: {kund} → målsida: {common_targets[target_idx]['target_url']}"
            )
            completed_targets += 1
        else:
            df.at[idx, "target_url"] = f"https://{canonical_root}"
            print(f"✓ Rad {idx}: {kund} → målsida (fallback): https://{canonical_root}")
            completed_targets += 1

    if needs_anchor:
        common_anchors = con.execute(
            """
            SELECT anchor_text, COUNT(*) as cnt
            FROM links_history
            WHERE customer_id = ? AND anchor_text IS NOT NULL AND anchor_text != ''
            AND length(anchor_text) > 2
            GROUP BY anchor_text
            ORDER BY cnt DESC
            LIMIT 30
        """,
            (customer_id,),
        ).fetchall()

        if common_anchors:
            # Rotera för variation
            anchor_idx = idx % len(common_anchors)
            selected_anchor = common_anchors[anchor_idx]["anchor_text"]
            df.at[idx, "link_anchor"] = selected_anchor
            print(f"✓ Rad {idx}: {kund} → ankar: '{selected_anchor}'")
            completed_anchors += 1
        else:
            df.at[idx, "link_anchor"] = customer["brand"] or kund
            print(
                f"✓ Rad {idx}: {kund} → ankar (fallback): '{customer['brand'] or kund}'"
            )
            completed_anchors += 1

con.close()

# Spara komplett CSV
df.to_csv(output_path, index=False, encoding="utf-8")

print("\n" + "=" * 70)
print("📊 RESULTAT")
print("=" * 70)
print(f"✅ Kompletterade målsidor: {completed_targets}/{original_needs_target}")
print(f"✅ Kompletterade ankartexter: {completed_anchors}/{original_needs_anchor}")
print(f"\n💾 Komplett plan sparad till: {output_path}")
print("\n🎉 NOVEMBER-PLANERINGEN ÄR NU KOMPLETT OCH REDO!")
