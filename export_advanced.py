        if brand_pattern.lower() in (stats['brand'] or '').lower()
    ]

    if not matching:
        print(f"[yellow]No customers found matching brand pattern: {brand_pattern}[/yellow]")
        return

    print(f"[cyan]Found {len(matching)} customers matching '{brand_pattern}':[/cyan]")
    for _, name, stats in matching:
        print(f"  • {name} ({stats['brand']})")

    if Confirm.ask("\nProceed with export?"):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_prefix = f"brand_{brand_pattern.replace(' ', '_')}"

        indices = [i + 1 for i, (db, name, stats) in enumerate(all_customers) if (db, name, stats) in matching]
        export_specific_customers(indices, output_prefix)


def export_by_domain(domain_pattern: str):
    """Export all customers matching a domain pattern."""
    all_customers = get_all_customer_dbs()

    matching = [
        (db, name, stats) for db, name, stats in all_customers
        if domain_pattern.lower() in (stats['canonical_root'] or '').lower() or domain_pattern.lower() in name.lower()
    ]

    if not matching:
        print(f"[yellow]No customers found matching domain pattern: {domain_pattern}[/yellow]")
        return

    print(f"[cyan]Found {len(matching)} customers matching '{domain_pattern}':[/cyan]")
    for _, name, stats in matching:
        print(f"  • {name} ({stats['canonical_root']})")

    if Confirm.ask("\nProceed with export?"):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_prefix = f"domain_{domain_pattern.replace('.', '_')}"

        indices = [i + 1 for i, (db, name, stats) in enumerate(all_customers) if (db, name, stats) in matching]
        export_specific_customers(indices, output_prefix)


def interactive_mode():
    """Interactive mode for selecting and exporting customers."""
    console.print("\n[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]  Advanced Airtable Export Tool[/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")

    customers = list_customers()

    if not customers:
        print("[red]No customers found[/red]")
        return

    print("\n[cyan]Export Options:[/cyan]")
    print("  1. Export specific customers by number")
    print("  2. Export by brand name")
    print("  3. Export by domain pattern")
    print("  4. Export all customers")
    print("  5. Exit")

    choice = Prompt.ask("\nSelect option", choices=["1", "2", "3", "4", "5"], default="4")

    if choice == "1":
        indices_str = Prompt.ask("\nEnter customer numbers (comma-separated, e.g., 1,3,5-10)")
        indices = []

        for part in indices_str.split(','):
            part = part.strip()
            if '-' in part:
                start, end = part.split('-')
                indices.extend(range(int(start), int(end) + 1))
            else:
                indices.append(int(part))

        export_specific_customers(indices, "custom")

    elif choice == "2":
        brand = Prompt.ask("Enter brand name or pattern")
        export_by_brand(brand)

    elif choice == "3":
        domain = Prompt.ask("Enter domain or pattern")
        export_by_domain(domain)

    elif choice == "4":
        if Confirm.ask(f"\nExport all {len(customers)} customers?", default=True):
            indices = list(range(1, len(customers) + 1))
            export_specific_customers(indices, "all")

    elif choice == "5":
        print("[cyan]Exiting...[/cyan]")


def main():
    parser = argparse.ArgumentParser(description="Advanced Airtable CSV Export Tool")
    parser.add_argument('--list', action='store_true', help='List all customers')
    parser.add_argument('--customers', type=str, help='Export specific customers (e.g., 1,3,5-10)')
    parser.add_argument('--brand', type=str, help='Export by brand pattern')
    parser.add_argument('--domain', type=str, help='Export by domain pattern')
    parser.add_argument('--all', action='store_true', help='Export all customers')

    args = parser.parse_args()

    if args.list:
        list_customers()
    elif args.customers:
        indices = []
        for part in args.customers.split(','):
            part = part.strip()
            if '-' in part:
                start, end = part.split('-')
                indices.extend(range(int(start), int(end) + 1))
            else:
                indices.append(int(part))
        export_specific_customers(indices, "custom")
    elif args.brand:
        export_by_brand(args.brand)
    elif args.domain:
        export_by_domain(args.domain)
    elif args.all:
        customers = get_all_customer_dbs()
        indices = list(range(1, len(customers) + 1))
        export_specific_customers(indices, "all")
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
"""
Advanced export options for Airtable CSV export.

This script provides more granular control over what gets exported.
"""
from __future__ import annotations

import argparse
import csv
import sqlite3
from datetime import datetime
from pathlib import Path

from rich import print
from rich.console import Console
from rich.prompt import Confirm, Prompt
from rich.table import Table

ROOT = Path(__file__).resolve().parent
CUSTOMERS_DIR = ROOT / "data" / "output" / "customers"
EXPORT_DIR = ROOT / "data" / "output" / "airtable_export"

console = Console()


def get_all_customer_dbs() -> list[tuple[Path, str, dict]]:
    """Find all customer.db files and return (path, customer_name, stats) tuples."""
    if not CUSTOMERS_DIR.exists():
        print(f"[red]Customer directory not found: {CUSTOMERS_DIR}[/red]")
        return []

    customer_dbs = []
    for customer_dir in CUSTOMERS_DIR.iterdir():
        if customer_dir.is_dir():
            db_path = customer_dir / "customer.db"
            if db_path.exists():
                try:
                    con = sqlite3.connect(db_path)
                    con.row_factory = sqlite3.Row

                    customer = con.execute("SELECT * FROM customers LIMIT 1").fetchone()
                    total_links = con.execute("SELECT COUNT(*) as cnt FROM links_history").fetchone()['cnt']

                    stats = {
                        'canonical_root': customer['canonical_root'] if customer else '',
                        'brand': customer['brand'] if customer else '',
                        'total_links': total_links
                    }

                    con.close()
                    customer_dbs.append((db_path, customer_dir.name, stats))
                except Exception:
                    continue

    return sorted(customer_dbs, key=lambda x: x[1])


def list_customers():
    """Display a table of all customers."""
    customers = get_all_customer_dbs()

    table = Table(title=f"Available Customers ({len(customers)} total)")
    table.add_column("#", justify="right", style="cyan")
    table.add_column("Directory", style="green")
    table.add_column("Canonical Root", style="yellow")
    table.add_column("Brand", style="magenta")
    table.add_column("Links", justify="right", style="blue")

    for idx, (_, name, stats) in enumerate(customers, 1):
        table.add_row(
            str(idx),
            name,
            stats['canonical_root'] or "-",
            stats['brand'] or "-",
            f"{stats['total_links']:,}"
        )

    console.print(table)
    return customers


def export_specific_customers(customer_indices: list[int], output_prefix: str = "custom"):
    """Export only specific customers by their index."""
    all_customers = get_all_customer_dbs()

    selected_customers = []
    for idx in customer_indices:
        if 1 <= idx <= len(all_customers):
            selected_customers.append(all_customers[idx - 1])
        else:
            print(f"[yellow]Warning: Index {idx} is out of range (1-{len(all_customers)})[/yellow]")

    if not selected_customers:
        print("[red]No valid customers selected[/red]")
        return

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Export customers
    customers_file = EXPORT_DIR / f"{output_prefix}_customers_{timestamp}.csv"
    with open(customers_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Database_ID', 'Canonical_Root', 'Brand', 'Directory_Name', 'Created_At', 'Total_Links'])

        for db_path, customer_name, stats in selected_customers:
            con = sqlite3.connect(db_path)
            con.row_factory = sqlite3.Row
            customer = con.execute("SELECT * FROM customers LIMIT 1").fetchone()

            writer.writerow([
                customer['id'],
                customer['canonical_root'] or '',
                customer['brand'] or '',
                customer_name,
                customer['created_at'] or '',
                stats['total_links']
            ])
            con.close()

    print(f"[green]✓ Exported {len(selected_customers)} customers to: {customers_file}[/green]")

    # Export links
    links_file = EXPORT_DIR / f"{output_prefix}_links_{timestamp}.csv"
    with open(links_file, 'w', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'Link_ID', 'Customer_ID', 'Customer_Name', 'Canonical_Root', 'Brand',
            'Pub_Page_URL', 'Pub_Domain', 'Target_URL', 'Target_Domain', 'Anchor_Text',
            'Link_Type', 'Language', 'Published_At', 'Created_At'
        ])

        total_links = 0
        for db_path, customer_name, stats in selected_customers:
            con = sqlite3.connect(db_path)
            con.row_factory = sqlite3.Row

            customer = con.execute("SELECT * FROM customers LIMIT 1").fetchone()
            links = con.execute("SELECT * FROM links_history ORDER BY id").fetchall()

            for link in links:
                writer.writerow([
                    link['id'],
                    link['customer_id'],
                    customer_name,
                    customer['canonical_root'] if customer else '',
                    customer['brand'] if customer else '',
                    link['pub_page_url'] or '',
                    link['pub_domain'] or '',
                    link['target_url'] or '',
                    link['target_domain'] or '',
                    link['anchor_text'] or '',
                    link['link_type'] or '',
                    link['language'] or '',
                    link['published_at'] or '',
                    link['created_at'] or ''
                ])
                total_links += 1

            con.close()

    print(f"[green]✓ Exported {total_links:,} links to: {links_file}[/green]")
    print(f"\n[cyan]Export location:[/cyan] {EXPORT_DIR}")


def export_by_brand(brand_pattern: str):
    """Export all customers matching a brand pattern."""
    all_customers = get_all_customer_dbs()

    matching = [
        (db, name, stats) for db, name, stats in all_customers

