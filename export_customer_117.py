"""
Exportera alla rader för customer_id 117 till CSV
"""
import sqlite3
import csv
from pathlib import Path
from datetime import datetime

# Databas och customer_id
HISTORY_DB = Path(r"C:\Users\robin\PycharmProjects\linkdb\data\output\linkops_history.db")
CUSTOMER_ID = 117
OUTPUT_DIR = Path(r"C:\Users\robin\PycharmProjects\linkdb\data\output")

print(f"Exporterar data för customer_id: {CUSTOMER_ID}")
print()

# Anslut till databasen
con = sqlite3.connect(HISTORY_DB)
con.row_factory = sqlite3.Row

# Hämta customer info
customer = con.execute("SELECT * FROM customers WHERE id=?", (CUSTOMER_ID,)).fetchone()
if not customer:
    print(f"ERROR: Customer ID {CUSTOMER_ID} finns inte!")
    exit(1)

print(f"Kund: {customer['canonical_root']} (Brand: {customer['brand']})")
print()

# Hämta alla länkar för denna kund
links = con.execute("""
    SELECT * FROM links_history 
    WHERE customer_id = ? 
    ORDER BY id
""", (CUSTOMER_ID,)).fetchall()

print(f"Antal länkar hittade: {len(links)}")

if len(links) == 0:
    print("Inga länkar att exportera!")
    exit(0)

# Skapa CSV-fil
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
csv_filename = OUTPUT_DIR / f"customer_{CUSTOMER_ID}_{customer['canonical_root'].replace('.', '_')}_{timestamp}.csv"

print(f"Exporterar till: {csv_filename}")
print()

# Skriv CSV
with open(csv_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
    # Hämta kolumnnamn från första raden
    column_names = links[0].keys()

    writer = csv.DictWriter(csvfile, fieldnames=column_names)

    # Skriv header (kolumnrubriker)
    writer.writeheader()

    # Skriv alla rader
    for link in links:
        writer.writerow(dict(link))

print(f"✅ Klart!")
print(f"   Exporterade: {len(links)} rader")
print(f"   Kolumner: {len(column_names)}")
print(f"   Fil: {csv_filename.name}")
print()
print("Kolumner i exporten:")
for i, col in enumerate(column_names, 1):
    print(f"  {i:2d}. {col}")

con.close()

