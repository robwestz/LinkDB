"""
Generiskt verktyg: Exportera data för vilket customer_id som helst till CSV
"""

import csv
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Databas
HISTORY_DB = Path(
    r"C:\Users\robin\PycharmProjects\linkdb\data\output\linkops_history.db"
)
OUTPUT_DIR = Path(r"C:\Users\robin\PycharmProjects\linkdb\data\output")


def export_customer_to_csv(customer_id: int):
    """Exportera alla länkar för en kund till CSV med kolumnrubriker."""

    print(f"Exporterar data för customer_id: {customer_id}")
    print()

    # Anslut till databasen
    con = sqlite3.connect(HISTORY_DB)
    con.row_factory = sqlite3.Row

    # Hämta customer info
    customer = con.execute(
        "SELECT * FROM customers WHERE id=?", (customer_id,)
    ).fetchone()
    if not customer:
        print(f"❌ ERROR: Customer ID {customer_id} finns inte!")
        con.close()
        return None

    print(f"Kund: {customer['canonical_root']} (Brand: {customer['brand']})")
    print()

    # Hämta alla länkar för denna kund
    links = con.execute(
        """
        SELECT * FROM links_history 
        WHERE customer_id = ? 
        ORDER BY id
    """,
        (customer_id,),
    ).fetchall()

    print(f"Antal länkar hittade: {len(links)}")

    if len(links) == 0:
        print("⚠ Inga länkar att exportera!")
        con.close()
        return None

    # Skapa CSV-fil med säkert filnamn
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = customer["canonical_root"].replace(".", "_").replace("/", "_")
    csv_filename = OUTPUT_DIR / f"customer_{customer_id}_{safe_name}_{timestamp}.csv"

    print(f"Exporterar till: {csv_filename.name}")
    print()

    # Skriv CSV
    with open(csv_filename, "w", newline="", encoding="utf-8-sig") as csvfile:
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
    return csv_filename


def list_customers():
    """Lista alla kunder med ID och namn."""
    con = sqlite3.connect(HISTORY_DB)
    con.row_factory = sqlite3.Row

    customers = con.execute(
        """
        SELECT c.id, c.canonical_root, c.brand, COUNT(lh.id) as link_count
        FROM customers c
        LEFT JOIN links_history lh ON c.id = lh.customer_id
        GROUP BY c.id
        ORDER BY c.id
    """
    ).fetchall()

    print(f"\n{'ID':<6} {'Canonical Root':<35} {'Brand':<25} {'Links':>6}")
    print("=" * 80)
    for cust in customers:
        print(
            f"{cust['id']:<6} {cust['canonical_root']:<35} {cust['brand'] or '-':<25} {cust['link_count']:>6}"
        )

    con.close()
    print(f"\nTotalt: {len(customers)} kunder")


def main():
    if len(sys.argv) < 2:
        print("Användning:")
        print("  python export_customer_by_id.py <customer_id>")
        print("  python export_customer_by_id.py --list")
        print()
        print("Exempel:")
        print("  python export_customer_by_id.py 117")
        print("  python export_customer_by_id.py --list")
        return

    if sys.argv[1] == "--list":
        list_customers()
    else:
        try:
            customer_id = int(sys.argv[1])
            csv_file = export_customer_to_csv(customer_id)
            if csv_file:
                print(f"\n📁 Fil: {csv_file}")
        except ValueError:
            print(f"❌ ERROR: '{sys.argv[1]}' är inte ett giltigt customer_id")


if __name__ == "__main__":
    main()
