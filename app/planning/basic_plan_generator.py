"""
Basic Plan Generator - Första versionen av intelligent länkplanering.

Använder:
- Volume detection (antal länkar från planeringsdokument)
- Historical analysis (vad har fungerat tidigare)
- Monthly patterns (hur har vi planerat tidigare månader)
- Strategy classification (vilken strategi passar)

Detta är GRUNDEN - semantisk analys läggs till i Fas 2.
"""

from __future__ import annotations

import random
import sqlite3
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from app.analyzers.link_history_analyzer import LinkHistoryAnalyzer
from app.analyzers.monthly_link_viewer import MonthlyLinkViewer
from app.planning.volume_detector import CustomerPlanningVolume, PlanningVolumeDetector


@dataclass
class PlannedLink:
    """En planerad länk."""

    customer_id: int
    canonical_root: str
    target_url: str
    anchor_text: str
    anchor_type: str  # exact, partial, branded, generic, lsi
    priority_score: float
    reasoning: str  # Varför valdes denna länk/ankar

    def to_dict(self) -> Dict:
        """Konvertera till dictionary för export."""
        return {
            "customer_id": self.customer_id,
            "canonical_root": self.canonical_root,
            "target_url": self.target_url,
            "anchor_text": self.anchor_text,
            "anchor_type": self.anchor_type,
            "priority_score": self.priority_score,
            "reasoning": self.reasoning,
        }


@dataclass
class LinkPlan:
    """En komplett länkplan för en eller flera kunder."""

    plan_name: str
    created_at: datetime
    customers: List[CustomerPlanningVolume]
    planned_links: List[PlannedLink]
    strategy_summary: Dict[str, int]

    @property
    def total_links(self) -> int:
        return len(self.planned_links)

    @property
    def total_customers(self) -> int:
        return len(self.customers)


class BasicPlanGenerator:
    """
    Grundläggande plan generator.

    Använder befintlig data för att skapa en första version av intelligenta planer.
    Semantisk analys kommer i Fas 2.
    """

    # Anchor type distributions per strategi (från PLANNING_SYSTEM_SPEC.md)
    ANCHOR_DISTRIBUTIONS = {
        "single_focus": {"exact": 0.50, "branded": 0.50},
        "diversified_basics": {
            "exact": 0.20,
            "partial": 0.30,
            "branded": 0.30,
            "generic": 0.20,
        },
        "semantic_foundation": {
            "exact": 0.15,
            "partial": 0.35,
            "branded": 0.20,
            "generic": 0.20,
            "lsi": 0.10,
        },
        "topical_authority": {
            "exact": 0.10,
            "partial": 0.35,
            "branded": 0.20,
            "generic": 0.20,
            "lsi": 0.15,
        },
        "enterprise_authority": {
            "exact": 0.08,
            "partial": 0.37,
            "branded": 0.20,
            "generic": 0.20,
            "lsi": 0.15,
        },
    }

    def __init__(self, history_db_path: str):
        """
        Initialize generator.

        Args:
            history_db_path: Path till linkops_history.db
        """
        self.history_db_path = history_db_path
        self.volume_detector = PlanningVolumeDetector(history_db_path)

    def generate_plan(
        self,
        planning_data: Dict[int, int],
        target_urls: Optional[Dict[int, List[str]]] = None,
        plan_name: Optional[str] = None,
    ) -> LinkPlan:
        """
        Generera en länkplan.

        Args:
            planning_data: Dict med {customer_id: antal_länkar}
            target_urls: Optional dict med {customer_id: [urls]} - målsidor
            plan_name: Namn på planen

        Returns:
            LinkPlan
        """
        # Detektera volumes och strategier
        volumes = self.volume_detector.detect_from_dict(planning_data)

        # Generera länkar för varje kund
        all_planned_links = []

        for volume in volumes:
            customer_links = self._generate_links_for_customer(
                volume, target_urls.get(volume.customer_id) if target_urls else None
            )
            all_planned_links.extend(customer_links)

        # Räkna strategier
        strategy_summary = {}
        for volume in volumes:
            strategy = volume.recommended_strategy
            strategy_summary[strategy] = strategy_summary.get(strategy, 0) + 1

        # Skapa plan
        if plan_name is None:
            plan_name = f"Link Plan {datetime.now().strftime('%Y-%m-%d')}"

        plan = LinkPlan(
            plan_name=plan_name,
            created_at=datetime.now(),
            customers=volumes,
            planned_links=all_planned_links,
            strategy_summary=strategy_summary,
        )

        return plan

    def _generate_links_for_customer(
        self, volume: CustomerPlanningVolume, target_urls: Optional[List[str]] = None
    ) -> List[PlannedLink]:
        """
        Generera länkar för en specifik kund.

        Args:
            volume: CustomerPlanningVolume för kunden
            target_urls: Optional lista med målsidor

        Returns:
            List of PlannedLink
        """
        links = []

        # Hämta historical analysis för att informera våra val
        analyzer = LinkHistoryAnalyzer(self.history_db_path)
        analysis = analyzer.analyze_customer(volume.customer_id)

        # Om vi inte har target URLs, använd historiska mest länkade
        if not target_urls and analysis:
            target_urls = [url for url, count in analysis.most_linked_urls[:5]]

        if not target_urls:
            # Fallback: skapa placeholder
            target_urls = [
                f"https://{volume.canonical_root}/page-{i}" for i in range(1, 4)
            ]

        # Hämta anchor distribution för strategin
        anchor_dist = self.ANCHOR_DISTRIBUTIONS.get(
            volume.recommended_strategy, self.ANCHOR_DISTRIBUTIONS["diversified_basics"]
        )

        # Generera länkar enligt distribution
        anchors_to_generate = self._calculate_anchor_counts(
            volume.planned_links, anchor_dist
        )

        # Skapa länkar
        for anchor_type, count in anchors_to_generate.items():
            for i in range(count):
                # Välj target URL (rotera genom listan)
                target_url = target_urls[i % len(target_urls)]

                # Generera anchor text baserat på type
                anchor_text = self._generate_anchor_text(
                    anchor_type, volume.canonical_root, target_url, analysis
                )

                # Beräkna priority (enkel version)
                priority = self._calculate_priority(
                    anchor_type, i, volume.planned_links
                )

                # Skapa reasoning
                reasoning = self._create_reasoning(
                    anchor_type, volume.recommended_strategy, analysis
                )

                link = PlannedLink(
                    customer_id=volume.customer_id,
                    canonical_root=volume.canonical_root,
                    target_url=target_url,
                    anchor_text=anchor_text,
                    anchor_type=anchor_type,
                    priority_score=priority,
                    reasoning=reasoning,
                )

                links.append(link)

        return links

    def _calculate_anchor_counts(
        self, total_links: int, distribution: Dict[str, float]
    ) -> Dict[str, int]:
        """Beräkna antal länkar per anchor type."""
        counts = {}
        remaining = total_links

        # Sortera för konsistens
        sorted_types = sorted(distribution.items(), key=lambda x: x[1], reverse=True)

        for anchor_type, percentage in sorted_types[:-1]:
            count = round(total_links * percentage)
            counts[anchor_type] = count
            remaining -= count

        # Sista typen får resterande
        last_type = sorted_types[-1][0]
        counts[last_type] = max(0, remaining)

        return counts

    def _generate_anchor_text(
        self, anchor_type: str, canonical_root: str, target_url: str, analysis
    ) -> str:
        """Generera anchor text baserat på type."""
        brand = canonical_root.replace(".com", "").replace(".se", "").title()

        if anchor_type == "exact":
            # Använd historical anchors om möjligt
            if analysis and analysis.most_common_anchors:
                return analysis.most_common_anchors[0][0]
            return f"{brand} erbjudande"

        elif anchor_type == "partial":
            return f"{brand} online"

        elif anchor_type == "branded":
            return brand

        elif anchor_type == "generic":
            generics = ["läs mer", "klicka här", "besök sidan", "här", "mer info"]
            return random.choice(generics)

        elif anchor_type == "lsi":
            return f"bästa {brand.lower()}"

        elif anchor_type == "naked_url":
            return canonical_root

        return brand

    def _calculate_priority(self, anchor_type: str, position: int, total: int) -> float:
        """Beräkna priority score (0-1)."""
        # Exact match får högre priority
        base_priority = {
            "exact": 0.9,
            "partial": 0.8,
            "lsi": 0.75,
            "branded": 0.7,
            "generic": 0.5,
        }.get(anchor_type, 0.5)

        # Justera baserat på position (tidigare = högre priority)
        position_factor = 1.0 - (position / total * 0.2)

        return min(base_priority * position_factor, 1.0)

    def _create_reasoning(self, anchor_type: str, strategy: str, analysis) -> str:
        """Skapa förklaring för valet."""
        reasons = []

        reasons.append(f"Strategi: {strategy}")
        reasons.append(f"Anchor type: {anchor_type}")

        if analysis:
            reasons.append(f"Baserat på historik med {analysis.total_links} länkar")

        return " | ".join(reasons)

    def export_to_csv(self, plan: LinkPlan, output_path: str):
        """Exportera plan till CSV."""
        import csv

        with open(output_path, "w", newline="", encoding="utf-8-sig") as csvfile:
            fieldnames = [
                "customer_id",
                "canonical_root",
                "target_url",
                "anchor_text",
                "anchor_type",
                "priority_score",
                "reasoning",
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for link in plan.planned_links:
                writer.writerow(link.to_dict())

        print(f"✅ Exporterade {plan.total_links} länkar till {output_path}")

    def print_plan_summary(self, plan: LinkPlan):
        """Skriv ut sammanfattning av planen."""
        print("\n" + "=" * 70)
        print(f"LINK PLAN: {plan.plan_name}")
        print("=" * 70)

        print(f"\n📊 ÖVERSIKT")
        print(f"  Skapad: {plan.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"  Kunder: {plan.total_customers}")
        print(f"  Totalt länkar: {plan.total_links}")

        print(f"\n🎯 STRATEGIER")
        for strategy, count in sorted(plan.strategy_summary.items()):
            print(f"  {strategy}: {count} kunder")

        print(f"\n📋 PER KUND")
        print("-" * 70)

        for customer in plan.customers:
            customer_links = [
                l for l in plan.planned_links if l.customer_id == customer.customer_id
            ]

            print(f"\n{customer.canonical_root} ({len(customer_links)} länkar)")
            print(f"  Strategi: {customer.recommended_strategy}")

            # Räkna anchor types
            anchor_counts = {}
            for link in customer_links:
                anchor_counts[link.anchor_type] = (
                    anchor_counts.get(link.anchor_type, 0) + 1
                )

            print(f"  Anchor distribution:")
            for atype, count in sorted(anchor_counts.items()):
                pct = (count / len(customer_links)) * 100
                print(f"    {atype}: {count} ({pct:.0f}%)")


def demo():
    """Demo av Basic Plan Generator."""
    from pathlib import Path

    # Hitta database
    db_path = (
        Path(__file__).resolve().parents[2] / "data" / "output" / "linkops_history.db"
    )

    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}")
        return

    generator = BasicPlanGenerator(str(db_path))

    # Simulera data från planeringsdokument
    planning_data = {
        117: 15,  # bethard.com med 15 länkar
    }

    # Generera plan
    print("🎯 Genererar länkplan...")
    plan = generator.generate_plan(
        planning_data=planning_data, plan_name="Test Plan November 2025"
    )

    # Visa sammanfattning
    generator.print_plan_summary(plan)

    # Exportera till CSV
    output_path = (
        Path(__file__).resolve().parents[2] / "data" / "output" / "test_link_plan.csv"
    )
    generator.export_to_csv(plan, str(output_path))

    print(f"\n📁 Plan exporterad till: {output_path}")


if __name__ == "__main__":
    demo()
