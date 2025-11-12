"""
Match customer_id from database to client_index
"""
import sqlite3
import pandas as pd
from pathlib import Path

# Paths
data_dir = Path(__file__).parent
db_path = data_dir / "output" / "linkops_history.db"
client_index_path = data_dir / "client_index.xlsx"

# Read client index
df = pd.read_excel(client_index_path)
print(f"Loaded {len(df)} rows from client_index.xlsx")
print(f"Columns: {df.columns.tolist()}")

# Connect to database
con = sqlite3.connect(db_path)
con.row_factory = sqlite3.Row

# Match customer_id for each customer_name
matched = 0
not_found = []

for idx, row in df.iterrows():
    customer_name = row.get('customer_name', '')

    if pd.isna(customer_name) or not customer_name:
        continue

    # Try to find customer_id
    customer = None

    # Method 1: Exact match on canonical_root
    customer = con.execute(
        "SELECT id, canonical_root FROM customers WHERE canonical_root = ?",
        (customer_name,)
    ).fetchone()

    # Method 2: LIKE match on canonical_root
    if not customer:
        customer = con.execute(
            "SELECT id, canonical_root FROM customers WHERE canonical_root LIKE ?",
            (f'%{customer_name}%',)
        ).fetchone()

    # Method 3: Match on brand
    if not customer:
        customer = con.execute(
            "SELECT id, canonical_root FROM customers WHERE brand LIKE ?",
            (f'%{customer_name}%',)
        ).fetchone()

    if customer:
        df.at[idx, 'customer_id'] = customer['id']
        matched += 1
        print(f"✓ {customer_name} → customer_id: {customer['id']}")
    else:
        not_found.append(customer_name)
        print(f"✗ {customer_name} → NOT FOUND")

con.close()

# Save updated file
output_path = data_dir / "client_index_matched.xlsx"
df.to_excel(output_path, index=False)

print(f"\n{'='*70}")
print(f"RESULTAT:")
print(f"{'='*70}")
print(f"Matchade: {matched}")
print(f"Ej funna: {len(not_found)}")
print(f"\nSparade till: {output_path}")

if not_found:
    print(f"\nEj funna kunder:")
    for name in not_found:
        print(f"  - {name}")

