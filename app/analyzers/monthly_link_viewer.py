"""
Monthly Link View - Visa länkar grupperade per månad för varje kund.

Detta ger oss gratis historik över hur varje månadsplanering har sett ut,
vilket blir en pusselbit i semantisk analys och topical authority-planering.
"""

from __future__ import annotations

import calendar
import sqlite3
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class MonthlyLinkGroup:
    """En grupp av länkar för en specifik månad."""

    year: int
    month: int
    month_name: str
    link_count: int
    links: List[sqlite3.Row]

    # Aggregerad statistik för månaden
    unique_pub_domains: int
    unique_target_urls: int
    anchor_types: Dict[str, int]
    most_common_anchors: List[tuple]
    target_url_distribution: List[tuple]

    @property
    def period(self) -> str:
        """Returnera period som string, t.ex. '2024-10'."""
        return f"{self.year}-{self.month:02d}"

    @property
    def display_name(self) -> str:
        """Returnera läsbart namn, t.ex. 'Oktober 2024'."""
        return f"{self.month_name} {self.year}"


class MonthlyLinkViewer:
    """
    Visar länkar grupperade per månad för en kund.
    Ger historik över alla månadsplaneringar som gjorts.
    """

    def __init__(self, customer_db_path: str):
        """
        Initialize viewer.

        Args:
            customer_db_path: Path till kundens customer.db
        """
        self.db_path = Path(customer_db_path)

        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found: {self.db_path}")

    def get_monthly_groups(self) -> List[MonthlyLinkGroup]:
        """
        Hämta alla länkar grupperade per månad.

        Returns:
            List of MonthlyLinkGroup, sorterade kronologiskt
        """
        con = sqlite3.connect(self.db_path)
        con.row_factory = sqlite3.Row

        # Hämta alla länkar med datum
        links = con.execute(
            """
            SELECT *,
                   COALESCE(published_at, created_at) as effective_date
            FROM links_history
            ORDER BY effective_date
        """
        ).fetchall()

        if not links:
            con.close()
            return []

        # Gruppera per månad
        monthly_dict = defaultdict(list)

        for link in links:
            date_str = link["effective_date"]
            if not date_str:
                continue

            try:
                # Parse datum
                if isinstance(date_str, str):
                    date_obj = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                else:
                    continue

                year_month = (date_obj.year, date_obj.month)
                monthly_dict[year_month].append(link)
            except:
                continue

        # Skapa MonthlyLinkGroup för varje månad
        groups = []

        for (year, month), month_links in sorted(monthly_dict.items()):
            # Beräkna statistik för månaden
            pub_domains = set()
            target_urls = set()
            anchor_types = defaultdict(int)
            anchors = []
            target_url_counts = defaultdict(int)

            for link in month_links:
                if link["pub_domain"]:
                    pub_domains.add(link["pub_domain"])
                if link["target_url"]:
                    target_urls.add(link["target_url"])
                    target_url_counts[link["target_url"]] += 1
                if link["anchor_type"]:
                    anchor_types[link["anchor_type"]] += 1
                if link["anchor_text"]:
                    anchors.append(link["anchor_text"])

            # Räkna vanligaste ankartexter
            from collections import Counter

            anchor_counter = Counter(anchors)
            most_common_anchors = anchor_counter.most_common(5)

            # Target URL distribution
            target_url_distribution = sorted(
                target_url_counts.items(), key=lambda x: x[1], reverse=True
            )[:5]

            month_name = calendar.month_name[month]

            group = MonthlyLinkGroup(
                year=year,
                month=month,
                month_name=month_name,
                link_count=len(month_links),
                links=month_links,
                unique_pub_domains=len(pub_domains),
                unique_target_urls=len(target_urls),
                anchor_types=dict(anchor_types),
                most_common_anchors=most_common_anchors,
                target_url_distribution=target_url_distribution,
            )

            groups.append(group)

        con.close()
        return groups

    def get_month(self, year: int, month: int) -> Optional[MonthlyLinkGroup]:
        """
        Hämta länkar för en specifik månad.

        Args:
            year: År (t.ex. 2024)
            month: Månad (1-12)

        Returns:
            MonthlyLinkGroup eller None om ingen data finns
        """
        groups = self.get_monthly_groups()

        for group in groups:
            if group.year == year and group.month == month:
                return group

        return None

    def get_recent_months(self, n: int = 6) -> List[MonthlyLinkGroup]:
        """
        Hämta de senaste N månaderna.

        Args:
            n: Antal månader att hämta

        Returns:
            List of MonthlyLinkGroup
        """
        groups = self.get_monthly_groups()
        return groups[-n:] if len(groups) > n else groups

    def print_summary(self):
        """Skriv ut en snygg sammanfattning av alla månader."""
        groups = self.get_monthly_groups()

        if not groups:
            print("Ingen länkdata hittad")
            return

        # Hämta customer info
        con = sqlite3.connect(self.db_path)
        con.row_factory = sqlite3.Row
        customer = con.execute("SELECT * FROM customers LIMIT 1").fetchone()
        con.close()

        print("\n" + "=" * 70)
        print(f"MONTHLY LINK HISTORY: {customer['canonical_root']}")
        print("=" * 70)

        print(f"\nTotalt: {len(groups)} månader med länkdata")
        print(f"Period: {groups[0].display_name} - {groups[-1].display_name}")
        print(f"Totalt länkar: {sum(g.link_count for g in groups)}")

        print("\n" + "-" * 70)
        print("MÅNADSÖVERSIKT")
        print("-" * 70)

        for group in groups:
            print(f"\n📅 {group.display_name} ({group.link_count} länkar)")
            print(f"   Publiceringsdomäner: {group.unique_pub_domains}")
            print(f"   Unika målsidor: {group.unique_target_urls}")

            if group.anchor_types:
                print(
                    f"   Anchor types: {', '.join(f'{k}: {v}' for k, v in group.anchor_types.items())}"
                )

            if group.most_common_anchors:
                top_anchor = group.most_common_anchors[0]
                print(f'   Vanligaste ankar: "{top_anchor[0]}" ({top_anchor[1]}x)')

            if group.target_url_distribution:
                top_url = group.target_url_distribution[0]
                print(f"   Mest länkad URL: {top_url[0][:50]}... ({top_url[1]}x)")

    def print_month_details(self, year: int, month: int):
        """Skriv ut detaljerad info för en specifik månad."""
        group = self.get_month(year, month)

        if not group:
            print(f"Ingen data för {year}-{month:02d}")
            return

        print("\n" + "=" * 70)
        print(f"DETALJER: {group.display_name}")
        print("=" * 70)

        print(f"\n📊 ÖVERSIKT")
        print(f"  Totalt länkar: {group.link_count}")
        print(f"  Publiceringsdomäner: {group.unique_pub_domains}")
        print(f"  Unika målsidor: {group.unique_target_urls}")

        print(f"\n🎯 ANCHOR TYPES")
        if group.anchor_types:
            for atype, count in sorted(
                group.anchor_types.items(), key=lambda x: x[1], reverse=True
            ):
                pct = (count / group.link_count) * 100
                print(f"  {atype}: {count} ({pct:.1f}%)")

        print(f"\n📝 VANLIGASTE ANKARTEXTER")
        for anchor, count in group.most_common_anchors:
            print(f'  "{anchor}" ({count}x)')

        print(f"\n🔗 MEST LÄNKADE MÅLSIDOR")
        for url, count in group.target_url_distribution:
            print(f"  {count}x - {url}")

        print(f"\n📋 ALLA LÄNKAR ({group.link_count} st)")
        print("-" * 70)

        for i, link in enumerate(group.links, 1):
            print(f"\n{i}. {link['pub_domain']} → {link['target_url'][:60]}")
            print(f"   Ankar: \"{link['anchor_text']}\" ({link['anchor_type']})")
            print(f"   Publicerad: {link['published_at'] or link['created_at']}")

    def export_month_to_csv(self, year: int, month: int, output_path: str):
        """Exportera en månads länkar till CSV."""
        import csv

        group = self.get_month(year, month)

        if not group:
            print(f"Ingen data för {year}-{month:02d}")
            return

        with open(output_path, "w", newline="", encoding="utf-8-sig") as csvfile:
            if not group.links:
                return

            # Hämta kolumnnamn från första länken
            fieldnames = group.links[0].keys()

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for link in group.links:
                writer.writerow(dict(link))

        print(f"✅ Exporterade {group.link_count} länkar till {output_path}")


def demo():
    """Demo av Monthly Link Viewer."""
    from pathlib import Path

    # Hitta en kunddatabas (bethard.com)
    db_path = (
        Path(__file__).resolve().parents[2]
        / "data"
        / "output"
        / "customers"
        / "bethard.com"
        / "customer.db"
    )

    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}")
        return

    viewer = MonthlyLinkViewer(str(db_path))

    # Visa översikt
    viewer.print_summary()

    # Visa senaste månaderna
    print("\n\n" + "=" * 70)
    print("SENASTE 3 MÅNADERNA")
    print("=" * 70)

    recent = viewer.get_recent_months(3)
    for group in recent:
        print(f"\n{group.display_name}: {group.link_count} länkar")
        print(
            f"  Målsidor: {group.unique_target_urls}, Pub-domäner: {group.unique_pub_domains}"
        )


if __name__ == "__main__":
    demo()
