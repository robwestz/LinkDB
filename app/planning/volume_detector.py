"""
Planning Volume Detector - Detekterar automatiskt antal länkar att planera
baserat på antal rader per customer_id i planeringsdokument.

Detta möjliggör semantisk planering eftersom vi vet hur många länkar
vi har att jobba med för varje kund.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Optional
from collections import Counter
import sqlite3
from pathlib import Path


@dataclass
class CustomerPlanningVolume:
    """Volym-information för en kunds planering."""
    customer_id: int
    canonical_root: str
    brand: str
    planned_links: int  # Antal rader i planeringsdokument

    # Från historik (om tillgänglig)
    historical_total: int = 0
    historical_monthly_avg: float = 0.0
    last_month_count: int = 0

    # Strategirekommendation
    recommended_strategy: str = ""
    can_cluster: bool = False
    can_build_authority: bool = False

    # Semantisk planering möjlig?
    semantic_planning_possible: bool = False
    semantic_complexity: str = "basic"  # basic, intermediate, advanced

    def __str__(self):
        return f"{self.canonical_root}: {self.planned_links} länkar planerade"


class PlanningVolumeDetector:
    """
    Detekterar automatiskt volym för planering baserat på data i planeringsdokument.
    """

    def __init__(self, history_db_path: str):
        """
        Initialize detector.

        Args:
            history_db_path: Path till linkops_history.db
        """
        self.history_db_path = history_db_path

    def detect_from_dict(self, planning_data: Dict[int, int]) -> List[CustomerPlanningVolume]:
        """
        Detektera volym från en dictionary med customer_id -> count.

        Args:
            planning_data: Dict med {customer_id: antal_rader}

        Returns:
            List of CustomerPlanningVolume
        """
        con = sqlite3.connect(self.history_db_path)
        con.row_factory = sqlite3.Row

        volumes = []

        for customer_id, planned_count in planning_data.items():
            # Hämta customer info
            customer = con.execute(
                "SELECT canonical_root, brand FROM customers WHERE id = ?",
                (customer_id,)
            ).fetchone()

            if not customer:
                continue

            # Hämta historisk data
            historical_total = con.execute(
                "SELECT COUNT(*) as cnt FROM links_history WHERE customer_id = ?",
                (customer_id,)
            ).fetchone()['cnt']

            # Beräkna månadsgenomsnitt (approximation)
            historical_monthly_avg = historical_total / 12 if historical_total > 0 else 0

            # Klassificera strategi
            strategy, can_cluster, can_authority = self._classify_strategy(planned_count)

            # Semantisk planering möjlig?
            semantic_possible, complexity = self._assess_semantic_capability(
                planned_count,
                historical_total
            )

            volume = CustomerPlanningVolume(
                customer_id=customer_id,
                canonical_root=customer['canonical_root'],
                brand=customer['brand'] or customer['canonical_root'],
                planned_links=planned_count,
                historical_total=historical_total,
                historical_monthly_avg=historical_monthly_avg,
                recommended_strategy=strategy,
                can_cluster=can_cluster,
                can_build_authority=can_authority,
                semantic_planning_possible=semantic_possible,
                semantic_complexity=complexity
            )

            volumes.append(volume)

        con.close()

        # Sortera efter planned_links (descending)
        volumes.sort(key=lambda x: x.planned_links, reverse=True)

        return volumes

    def detect_from_planning_sheet(self, sheet_data: List[Dict]) -> List[CustomerPlanningVolume]:
        """
        Detektera volym från parsed sheet data.

        Args:
            sheet_data: List av dictionaries från planeringsdokument
                       Varje dict måste ha 'customer_id' eller 'brand'/'canonical_root'

        Returns:
            List of CustomerPlanningVolume
        """
        # Räkna förekomster per customer_id eller brand
        customer_counts = Counter()

        for row in sheet_data:
            # Försök hitta customer_id
            customer_id = row.get('customer_id')

            if customer_id:
                customer_counts[customer_id] += 1
            else:
                # Fallback: försök matcha via brand/canonical_root
                brand = row.get('brand') or row.get('canonical_root')
                if brand:
                    # Slå upp customer_id via brand
                    cid = self._lookup_customer_id(brand)
                    if cid:
                        customer_counts[cid] += 1

        return self.detect_from_dict(dict(customer_counts))

    def _lookup_customer_id(self, identifier: str) -> Optional[int]:
        """Slå upp customer_id från brand eller canonical_root."""
        con = sqlite3.connect(self.history_db_path)

        result = con.execute("""
            SELECT id FROM customers 
            WHERE canonical_root = ? OR brand = ?
            LIMIT 1
        """, (identifier, identifier)).fetchone()

        con.close()

        return result[0] if result else None

    def _classify_strategy(self, link_count: int) -> tuple[str, bool, bool]:
        """
        Klassificera strategi baserat på antal länkar.

        Returns:
            (strategy_name, can_cluster, can_build_authority)
        """
        if link_count == 1:
            return ("single_focus", False, False)
        elif link_count <= 5:
            return ("diversified_basics", False, False)
        elif link_count <= 15:
            return ("semantic_foundation", True, True)
        elif link_count <= 30:
            return ("topical_authority", True, True)
        else:
            return ("enterprise_authority", True, True)

    def _assess_semantic_capability(
        self,
        planned_count: int,
        historical_count: int
    ) -> tuple[bool, str]:
        """
        Bedöm om semantisk planering är möjlig och hur avancerad.

        Returns:
            (is_possible, complexity_level)
        """
        # Minst 6 länkar krävs för semantisk planering
        if planned_count < 6:
            return (False, "basic")

        # Med 6-15 länkar: intermediate semantics
        if planned_count <= 15:
            return (True, "intermediate")

        # Med 16+ länkar och historik: advanced semantics
        if planned_count >= 16:
            if historical_count > 20:
                return (True, "advanced_with_history")
            else:
                return (True, "advanced")

        return (False, "basic")

    def print_summary(self, volumes: List[CustomerPlanningVolume]):
        """Skriv ut sammanfattning av detected volumes."""
        print("\n" + "="*70)
        print("PLANNING VOLUME DETECTION")
        print("="*70)

        total_customers = len(volumes)
        total_links = sum(v.planned_links for v in volumes)

        print(f"\n📊 ÖVERSIKT")
        print(f"  Totalt kunder: {total_customers}")
        print(f"  Totalt länkar att planera: {total_links}")
        print(f"  Genomsnitt per kund: {total_links / total_customers:.1f}")

        # Gruppera per strategi
        from collections import defaultdict
        strategy_groups = defaultdict(list)

        for v in volumes:
            strategy_groups[v.recommended_strategy].append(v)

        print(f"\n🎯 STRATEGIFÖRDELNING")
        for strategy, group in sorted(strategy_groups.items()):
            print(f"  {strategy}: {len(group)} kunder ({sum(v.planned_links for v in group)} länkar)")

        # Semantisk kapacitet
        semantic_capable = [v for v in volumes if v.semantic_planning_possible]

        print(f"\n🧠 SEMANTISK PLANERING")
        print(f"  Möjlig för: {len(semantic_capable)}/{total_customers} kunder")

        if semantic_capable:
            complexity_counts = Counter(v.semantic_complexity for v in semantic_capable)
            for complexity, count in complexity_counts.items():
                print(f"  {complexity}: {count} kunder")

        print(f"\n📋 DETALJERAD LISTA")
        print("-"*70)

        for v in volumes:
            print(f"\n{v.canonical_root}")
            print(f"  Planerade länkar: {v.planned_links}")
            print(f"  Historik: {v.historical_total} totalt, ~{v.historical_monthly_avg:.1f}/månad")
            print(f"  Strategi: {v.recommended_strategy}")
            print(f"  Semantisk planering: {'✅ Ja' if v.semantic_planning_possible else '❌ Nej'} ({v.semantic_complexity})")

            if v.semantic_planning_possible:
                print(f"  → Kan bygga topic clusters: {v.can_cluster}")
                print(f"  → Kan bygga topical authority: {v.can_build_authority}")


def demo():
    """Demo av Planning Volume Detector."""
    from pathlib import Path

    # Hitta history database
    db_path = Path(__file__).resolve().parents[2] / "data" / "output" / "linkops_history.db"

    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}")
        return

    detector = PlanningVolumeDetector(str(db_path))

    # Simulera data från planeringsdokument
    # I verkligheten kommer detta från Google Sheets
    planning_data = {
        117: 15,  # bethard.com med 15 länkar planerade
        # Lägg till fler om du har andra customer_ids
    }

    print("🔍 Detekterar planerings-volym från data...")
    volumes = detector.detect_from_dict(planning_data)

    detector.print_summary(volumes)

    print("\n\n" + "="*70)
    print("SEMANTISK PLANERING - MÖJLIGHETER")
    print("="*70)

    for v in volumes:
        if v.semantic_planning_possible:
            print(f"\n✨ {v.canonical_root}")
            print(f"   Med {v.planned_links} länkar kan vi:")

            if v.can_cluster:
                print(f"   ✅ Skapa semantiska kluster av relaterade målsidor")

            if v.can_build_authority:
                print(f"   ✅ Bygga topical authority inom specifika topics")

            print(f"   ✅ Optimera ankartexter för entiteter och sökfraser")
            print(f"   ✅ Koordinera länkar för maximal SEO-effekt")

            if v.semantic_complexity == "advanced_with_history":
                print(f"   🎯 BONUS: Kan använda historik för att förbättra planeringen!")


if __name__ == "__main__":
    demo()

