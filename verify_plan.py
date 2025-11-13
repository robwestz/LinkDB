"""
Verify November Plan - Kollar vad som fortfarande saknas
"""

import pandas as pd

df = pd.read_csv("november_plan_completed.csv")

print(f"📋 Totalt rader: {len(df)}")
print(f"✅ Har målsida: {df['target_url'].notna().sum()}")
print(f"✅ Har ankartext: {df['link_anchor'].notna().sum()}")

still_needs = df[(df["target_url"].isna()) | (df["link_anchor"].isna())]
print(f"\n⚠️  Fortfarande saknar data: {len(still_needs)} rader")

if len(still_needs) > 0:
    print("\nRader som behöver kompletteras:\n")
    for idx, row in still_needs.iterrows():
        print(
            f"Rad {idx}: {row['kund_brand']} på {row['publication_domain']} ({row['market']})"
        )
        if pd.isna(row["target_url"]):
            print(f"  ❌ Saknar målsida")
        if pd.isna(row["link_anchor"]):
            print(f"  ❌ Saknar ankartext")
        print()
else:
    print("\n🎉 ALLA LÄNKAR ÄR KOMPLETTA!")
