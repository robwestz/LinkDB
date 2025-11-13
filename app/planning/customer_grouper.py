"""
Customer Grouper - Grupperar kunder baserat på antal tillgängliga länkar
och tilldelar lämplig planeringsstrategi.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List


class LinkVolumeGroup(Enum):
    """Grupper baserade på antal länkar."""

    SINGLE = "single"  # 1 länk
    FEW = "few"  # 2-5 länkar
    MEDIUM = "medium"  # 6-15 länkar
    MANY = "many"  # 16-30 länkar
    BULK = "bulk"  # 31+ länkar


@dataclass
class CustomerGroup:
    """Representation av en kundgrupp."""

    customer_id: int
    canonical_root: str
    brand: str
    link_count: int
    volume_group: LinkVolumeGroup
    recommended_strategy: str
    can_build_authority: bool
    can_semantic_cluster: bool

    def __str__(self):
        return f"{self.canonical_root} ({self.link_count} links) - {self.volume_group.value}"


class CustomerGrouper:
    """
    Grupperar kunder baserat på antal tillgängliga länkar och
    rekommenderar strategier.
    """

    # Strategier per grupp
    STRATEGIES = {
        LinkVolumeGroup.SINGLE: {
            "name": "single_focus",
            "description": "Fokusera på en starkt optimerad länk",
            "anchor_strategy": "exact_or_branded",
            "can_cluster": False,
            "can_authority": False,
        },
        LinkVolumeGroup.FEW: {
            "name": "diversified_basics",
            "description": "Diversifiera ankartexter, grund för flera sidor",
            "anchor_strategy": "mixed_diversified",
            "can_cluster": False,
            "can_authority": False,
        },
        LinkVolumeGroup.MEDIUM: {
            "name": "semantic_foundation",
            "description": "Börja bygga semantiska kluster, grundläggande authority",
            "anchor_strategy": "semantic_aware",
            "can_cluster": True,
            "can_authority": True,
        },
        LinkVolumeGroup.MANY: {
            "name": "topical_authority",
            "description": "Full topical authority-strategi med flera kluster",
            "anchor_strategy": "advanced_semantic",
            "can_cluster": True,
            "can_authority": True,
        },
        LinkVolumeGroup.BULK: {
            "name": "enterprise_authority",
            "description": "Enterprise-strategi med djup topic coverage",
            "anchor_strategy": "comprehensive_semantic",
            "can_cluster": True,
            "can_authority": True,
        },
    }

    def __init__(self, db_path: str):
        """
        Initialize grouper.

        Args:
            db_path: Path to linkops_history.db
        """
        self.db_path = db_path

    def classify_by_volume(self, link_count: int) -> LinkVolumeGroup:
        """
        Klassificera baserat på antal länkar.

        Args:
            link_count: Antal länkar

        Returns:
            LinkVolumeGroup enum
        """
        if link_count == 1:
            return LinkVolumeGroup.SINGLE
        elif link_count <= 5:
            return LinkVolumeGroup.FEW
        elif link_count <= 15:
            return LinkVolumeGroup.MEDIUM
        elif link_count <= 30:
            return LinkVolumeGroup.MANY
        else:
            return LinkVolumeGroup.BULK

    def get_strategy(self, volume_group: LinkVolumeGroup) -> Dict:
        """
        Hämta rekommenderad strategi för en volymgrupp.

        Args:
            volume_group: LinkVolumeGroup

        Returns:
            Dictionary med strategiinfo
        """
        return self.STRATEGIES[volume_group]

    def group_customers(
        self, customer_link_counts: Dict[int, int]
    ) -> List[CustomerGroup]:
        """
        Gruppera kunder baserat på antal länkar.

        Args:
            customer_link_counts: Dict med {customer_id: link_count}

        Returns:
            List of CustomerGroup objects
        """
        con = sqlite3.connect(self.db_path)
        con.row_factory = sqlite3.Row

        groups = []

        for customer_id, link_count in customer_link_counts.items():
            # Hämta customer info
            customer = con.execute(
                "SELECT canonical_root, brand FROM customers WHERE id = ?",
                (customer_id,),
            ).fetchone()

            if not customer:
                continue

            # Klassificera
            volume_group = self.classify_by_volume(link_count)
            strategy = self.get_strategy(volume_group)

            group = CustomerGroup(
                customer_id=customer_id,
                canonical_root=customer["canonical_root"],
                brand=customer["brand"] or customer["canonical_root"],
                link_count=link_count,
                volume_group=volume_group,
                recommended_strategy=strategy["name"],
                can_build_authority=strategy["can_authority"],
                can_semantic_cluster=strategy["can_cluster"],
            )

            groups.append(group)

        con.close()

        # Sortera efter antal länkar (descending)
        groups.sort(key=lambda x: x.link_count, reverse=True)

        return groups

    def get_group_summary(self, groups: List[CustomerGroup]) -> Dict:
        """
        Skapa sammanfattning av grupperingen.

        Args:
            groups: List of CustomerGroup

        Returns:
            Dictionary med statistik
        """
        summary = {
            "total_customers": len(groups),
            "total_links": sum(g.link_count for g in groups),
            "groups": {},
            "strategies": {},
        }

        # Gruppera per volume group
        for volume_group in LinkVolumeGroup:
            group_customers = [g for g in groups if g.volume_group == volume_group]
            if group_customers:
                summary["groups"][volume_group.value] = {
                    "count": len(group_customers),
                    "total_links": sum(g.link_count for g in group_customers),
                    "customers": [g.canonical_root for g in group_customers],
                }

        # Gruppera per strategi
        for group in groups:
            strategy = group.recommended_strategy
            if strategy not in summary["strategies"]:
                summary["strategies"][strategy] = {
                    "count": 0,
                    "total_links": 0,
                    "customers": [],
                }
            summary["strategies"][strategy]["count"] += 1
            summary["strategies"][strategy]["total_links"] += group.link_count
            summary["strategies"][strategy]["customers"].append(group.canonical_root)

        return summary

    def print_summary(self, groups: List[CustomerGroup]):
        """
        Skriv ut en snygg sammanfattning.

        Args:
            groups: List of CustomerGroup
        """
        summary = self.get_group_summary(groups)

        print("\n" + "=" * 70)
        print("CUSTOMER GROUPING SUMMARY")
        print("=" * 70)
        print(f"\nTotal Customers: {summary['total_customers']}")
        print(f"Total Links: {summary['total_links']}")

        print("\n" + "-" * 70)
        print("GROUPS BY VOLUME")
        print("-" * 70)

        for volume_group in LinkVolumeGroup:
            group_key = volume_group.value
            if group_key in summary["groups"]:
                data = summary["groups"][group_key]
                strategy = self.STRATEGIES[volume_group]
                print(
                    f"\n{volume_group.value.upper()} ({data['count']} customers, {data['total_links']} links)"
                )
                print(f"  Strategy: {strategy['name']}")
                print(f"  Description: {strategy['description']}")
                print(f"  Can cluster: {strategy['can_cluster']}")
                print(f"  Can build authority: {strategy['can_authority']}")
                if data["count"] <= 5:
                    print(f"  Customers: {', '.join(data['customers'])}")

        print("\n" + "-" * 70)
        print("RECOMMENDED STRATEGIES")
        print("-" * 70)

        for strategy_name, data in summary["strategies"].items():
            print(
                f"\n{strategy_name.upper()} ({data['count']} customers, {data['total_links']} links)"
            )
            if data["count"] <= 5:
                print(f"  Customers: {', '.join(data['customers'])}")


def demo():
    """Demo av Customer Grouper."""
    from pathlib import Path

    # Hitta databas
    db_path = (
        Path(__file__).resolve().parents[2] / "data" / "output" / "linkops_history.db"
    )

    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}")
        return

    # Simulera att vi har ett planeringsdokument med olika kunder
    # I verkligheten kommer detta från Google Sheets
    sample_counts = {
        117: 15,  # bethard.com - MEDIUM
        50: 1,  # någon annan - SINGLE
        75: 8,  # någon annan - MEDIUM
        100: 25,  # någon annan - MANY
        # etc...
    }

    grouper = CustomerGrouper(str(db_path))
    groups = grouper.group_customers(sample_counts)

    grouper.print_summary(groups)

    print("\n" + "=" * 70)
    print("INDIVIDUAL CUSTOMER DETAILS")
    print("=" * 70)

    for group in groups:
        print(f"\n{group}")
        print(f"  Strategy: {group.recommended_strategy}")
        print(f"  Can semantic cluster: {group.can_semantic_cluster}")
        print(f"  Can build authority: {group.can_build_authority}")


if __name__ == "__main__":
    demo()
