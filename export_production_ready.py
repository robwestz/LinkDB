"""
Export Production Ready Links - Exporterar endast kompletta länkar
"""

from pathlib import Path

import pandas as pd

# Läs den uppdaterade CSV:en
csv_path = Path(r"C:\Users\robin\Downloads\november_plan - november_plan (1).csv")
df = pd.read_csv(csv_path)

print(f"📋 Totalt rader: {len(df)}")

# Filtrera: Behåll bara rader med både publication_domain OCH kund_brand
df_ready = df[
    df["publication_domain"].notna()
    & (df["publication_domain"] != "")
    & df["kund_brand"].notna()
    & (df["kund_brand"] != "")
].copy()

print(f"✅ Kompletta länkar (har pub_domain + kund): {len(df_ready)}")

# Visa vilka som filtreras bort
df_incomplete = df[
    df["publication_domain"].isna()
    | (df["publication_domain"] == "")
    | df["kund_brand"].isna()
    | (df["kund_brand"] == "")
]

print(f"⚠️  Ofullständiga länkar (saknar pub_domain eller kund): {len(df_incomplete)}")

if len(df_incomplete) > 0:
    print("\nOfullständiga rader (väntar på kollega):")
    for idx, row in df_incomplete.iterrows():
        pub = row.get("publication_domain", "SAKNAS")
        kund = row.get("kund_brand", "SAKNAS")
        print(f"  Rad {idx}: pub_domain={pub}, kund={kund}")

# Statistik för de kompletta
print(f"\n📊 STATISTIK FÖR KOMPLETTA LÄNKAR:")
print(f"Totalt kompletta: {len(df_ready)}")
print(f"Unika kunder: {df_ready['kund_brand'].nunique()}")
print(f"Marknader: {df_ready['market'].value_counts().to_dict()}")

# Kolla vilka som har målsida och ankartext
has_target = df_ready["target_url"].notna().sum()
has_anchor = df_ready["link_anchor"].notna().sum()

print(f"\nHar målsida: {has_target}/{len(df_ready)}")
print(f"Har ankartext: {has_anchor}/{len(df_ready)}")

# Exportera till produktionsklar fil
output_path = Path(
    "C:/Users/robin/PycharmProjects/linkdb/november_plan_PRODUCTION_READY.csv"
)
df_ready.to_csv(output_path, index=False, encoding="utf-8")

print(f"\n💾 Exporterad till: {output_path}")
print(f"\n✅ {len(df_ready)} KOMPLETTA LÄNKAR REDO FÖR PRODUKTION!")

# Skapa också en Excel-version för enklare granskning
excel_path = Path(
    "C:/Users/robin/PycharmProjects/linkdb/november_plan_PRODUCTION_READY.xlsx"
)
df_ready.to_excel(excel_path, index=False, engine="openpyxl")
print(f"💾 Excel-version: {excel_path}")

# Visa sammanfattning per kund
print("\n📋 LÄNKAR PER KUND:")
kund_counts = df_ready["kund_brand"].value_counts()
for kund, count in kund_counts.items():
    print(f"  {kund}: {count} länkar")
