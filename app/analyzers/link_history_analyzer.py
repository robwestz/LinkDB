"""
Link History Analyzer - Analyserar historisk länkdata för att identifiera
mönster och framgångsrika strategier.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Dict, Optional
from collections import Counter
import sqlite3
from datetime import datetime, timedelta


@dataclass
class LinkAnalysis:
    """Resultat av länkanalys för en kund."""
    customer_id: int
    canonical_root: str
    brand: str

    # Grundläggande metrics
    total_links: int
    unique_pub_domains: int
    unique_target_domains: int
    unique_target_urls: int

    # Tidsbas era metrics
    first_link_date: Optional[str]
    last_link_date: Optional[str]
    days_active: int
    links_per_month: float

    # Anchor text analys
    anchor_types: Dict[str, int]
    most_common_anchors: List[tuple]  # [(anchor, count), ...]
    anchor_diversity_score: float  # 0-1, högre = mer diversifierad

    # Target analys
    most_linked_urls: List[tuple]  # [(url, count), ...]
    top_target_domains: List[tuple]  # [(domain, count), ...]

    # Länktyper
    link_types: Dict[str, int]
    languages: Dict[str, int]

    # Strategisk insikt
    primary_strategy: str  # Vilken strategi verkar de använda?
    recommendations: List[str]


class LinkHistoryAnalyzer:
    """
    Analyserar historisk länkdata för att hitta mönster och ge rekommendationer.
    """

    def __init__(self, db_path: str):
        """
        Initialize analyzer.

        Args:
            db_path: Path to linkops_history.db
        """
        self.db_path = db_path

    def analyze_customer(self, customer_id: int) -> Optional[LinkAnalysis]:
        """
        Analysera en specifik kund.

        Args:
            customer_id: Customer ID

        Returns:
            LinkAnalysis object eller None om ingen data finns
        """
        con = sqlite3.connect(self.db_path)
        con.row_factory = sqlite3.Row

        # Hämta customer info
        customer = con.execute(
            "SELECT canonical_root, brand FROM customers WHERE id = ?",
            (customer_id,)
        ).fetchone()

        if not customer:
            con.close()
            return None

        # Hämta alla länkar för kunden
        links = con.execute("""
            SELECT 
                pub_domain,
                target_url,
                target_domain,
                anchor_text,
                link_type,
                language,
                anchor_type,
                published_at,
                created_at
            FROM links_history
            WHERE customer_id = ?
            ORDER BY published_at, created_at
        """, (customer_id,)).fetchall()

        con.close()

        if not links:
            return None

        # Grundläggande räkningar
        total_links = len(links)
        unique_pub_domains = len(set(link['pub_domain'] for link in links if link['pub_domain']))
        unique_target_domains = len(set(link['target_domain'] for link in links if link['target_domain']))
        unique_target_urls = len(set(link['target_url'] for link in links if link['target_url']))

        # Tidsbas era metrics
        dates = [link['published_at'] or link['created_at'] for link in links if link['published_at'] or link['created_at']]
        if dates:
            dates_parsed = []
            for d in dates:
                try:
                    if isinstance(d, str):
                        dates_parsed.append(datetime.fromisoformat(d.replace('Z', '+00:00')))
                except:
                    pass

            if dates_parsed:
                first_date = min(dates_parsed)
                last_date = max(dates_parsed)
                days_active = (last_date - first_date).days + 1
                links_per_month = (total_links / days_active * 30) if days_active > 0 else 0
                first_link_str = first_date.strftime('%Y-%m-%d')
                last_link_str = last_date.strftime('%Y-%m-%d')
            else:
                first_link_str = None
                last_link_str = None
                days_active = 0
                links_per_month = 0
        else:
            first_link_str = None
            last_link_str = None
            days_active = 0
            links_per_month = 0

        # Anchor text analys
        anchors = [link['anchor_text'] for link in links if link['anchor_text']]
        anchor_counter = Counter(anchors)
        most_common_anchors = anchor_counter.most_common(10)

        # Anchor diversity (Shannon entropy approximation)
        if anchors:
            unique_anchors = len(set(anchors))
            anchor_diversity = min(unique_anchors / total_links, 1.0)
        else:
            anchor_diversity = 0.0

        # Anchor types
        anchor_types_list = [link['anchor_type'] for link in links if link['anchor_type']]
        anchor_types = dict(Counter(anchor_types_list))

        # Target analys
        target_urls = [link['target_url'] for link in links if link['target_url']]
        target_counter = Counter(target_urls)
        most_linked_urls = target_counter.most_common(10)

        target_domains = [link['target_domain'] for link in links if link['target_domain']]
        domain_counter = Counter(target_domains)
        top_target_domains = domain_counter.most_common(5)

        # Link types och languages
        link_types_list = [link['link_type'] for link in links if link['link_type']]
        link_types = dict(Counter(link_types_list))

        languages_list = [link['language'] for link in links if link['language']]
        languages = dict(Counter(languages_list))

        # Identifiera primär strategi
        primary_strategy = self._identify_strategy(
            total_links,
            anchor_diversity,
            anchor_types,
            most_linked_urls
        )

        # Generera rekommendationer
        recommendations = self._generate_recommendations(
            total_links,
            anchor_diversity,
            anchor_types,
            unique_target_urls,
            links_per_month
        )

        return LinkAnalysis(
            customer_id=customer_id,
            canonical_root=customer['canonical_root'],
            brand=customer['brand'] or customer['canonical_root'],
            total_links=total_links,
            unique_pub_domains=unique_pub_domains,
            unique_target_domains=unique_target_domains,
            unique_target_urls=unique_target_urls,
            first_link_date=first_link_str,
            last_link_date=last_link_str,
            days_active=days_active,
            links_per_month=links_per_month,
            anchor_types=anchor_types,
            most_common_anchors=most_common_anchors,
            anchor_diversity_score=anchor_diversity,
            most_linked_urls=most_linked_urls,
            top_target_domains=top_target_domains,
            link_types=link_types,
            languages=languages,
            primary_strategy=primary_strategy,
            recommendations=recommendations
        )

    def _identify_strategy(
        self,
        total_links: int,
        anchor_diversity: float,
        anchor_types: Dict[str, int],
        most_linked_urls: List[tuple]
    ) -> str:
        """Identifiera vilken strategi som används."""

        # Hög concentration på en URL = focused strategy
        if most_linked_urls and total_links > 0:
            top_url_ratio = most_linked_urls[0][1] / total_links
            if top_url_ratio > 0.5:
                return "focused_single_page"

        # Låg diversity = repetitive strategy
        if anchor_diversity < 0.3:
            return "repetitive_anchors"

        # Hög diversity = diversified strategy
        if anchor_diversity > 0.7:
            return "highly_diversified"

        # Många länkar med god diversity = authority building
        if total_links > 15 and anchor_diversity > 0.5:
            return "authority_building"

        return "balanced_approach"

    def _generate_recommendations(
        self,
        total_links: int,
        anchor_diversity: float,
        anchor_types: Dict[str, int],
        unique_target_urls: int,
        links_per_month: float
    ) -> List[str]:
        """Generera rekommendationer baserat på analys."""
        recommendations = []

        # Anchor diversity rekommendationer
        if anchor_diversity < 0.4:
            recommendations.append(
                "⚠️ Låg anchor diversity - öka variationen i ankartexter"
            )
        elif anchor_diversity > 0.9:
            recommendations.append(
                "✅ Utmärkt anchor diversity"
            )

        # URL diversity
        if unique_target_urls < 3 and total_links > 10:
            recommendations.append(
                "💡 Överväg att länka till fler olika målsidor för bättre topic coverage"
            )

        # Länkhastighet
        if links_per_month > 30:
            recommendations.append(
                "⚠️ Hög länkhastighet - var försiktig med naturlig länkbyggnad"
            )
        elif links_per_month < 2 and total_links > 5:
            recommendations.append(
                "💡 Låg länkhastighet - det finns utrymme att öka takten"
            )

        # Anchor type distribution
        if anchor_types:
            exact_ratio = anchor_types.get('exact', 0) / total_links
            if exact_ratio > 0.4:
                recommendations.append(
                    "⚠️ För många exact match anchors - diversifiera med partial/generic"
                )

        # Volym-baserade tips
        if total_links < 5:
            recommendations.append(
                "📈 Med fler länkar kan du börja bygga semantiska kluster"
            )
        elif total_links >= 15:
            recommendations.append(
                "🎯 Tillräcklig volym för topical authority-strategi"
            )

        if not recommendations:
            recommendations.append("✅ God balans i länkprofilen")

        return recommendations

    def print_analysis(self, analysis: LinkAnalysis):
        """Skriv ut en snygg analys."""
        print("\n" + "="*70)
        print(f"LINK HISTORY ANALYSIS: {analysis.canonical_root}")
        print("="*70)

        print(f"\n📊 OVERVIEW")
        print(f"  Brand: {analysis.brand}")
        print(f"  Total links: {analysis.total_links}")
        print(f"  Unique publishing domains: {analysis.unique_pub_domains}")
        print(f"  Unique target URLs: {analysis.unique_target_urls}")

        if analysis.first_link_date:
            print(f"\n📅 TIMELINE")
            print(f"  First link: {analysis.first_link_date}")
            print(f"  Last link: {analysis.last_link_date}")
            print(f"  Days active: {analysis.days_active}")
            print(f"  Links per month: {analysis.links_per_month:.1f}")

        print(f"\n🎯 ANCHOR TEXT ANALYSIS")
        print(f"  Diversity score: {analysis.anchor_diversity_score:.2f} (0-1, higher = more diverse)")

        if analysis.anchor_types:
            print(f"  Anchor types:")
            for atype, count in sorted(analysis.anchor_types.items(), key=lambda x: x[1], reverse=True):
                pct = (count / analysis.total_links) * 100
                print(f"    - {atype}: {count} ({pct:.1f}%)")

        if analysis.most_common_anchors:
            print(f"  Most common anchors:")
            for anchor, count in analysis.most_common_anchors[:5]:
                print(f"    - \"{anchor}\" ({count}x)")

        if analysis.most_linked_urls:
            print(f"\n🔗 TARGET URL ANALYSIS")
            print(f"  Most linked URLs:")
            for url, count in analysis.most_linked_urls[:5]:
                print(f"    - {url} ({count}x)")

        print(f"\n🎨 STRATEGY ANALYSIS")
        print(f"  Primary strategy: {analysis.primary_strategy}")

        print(f"\n💡 RECOMMENDATIONS")
        for rec in analysis.recommendations:
            print(f"  {rec}")


def demo():
    """Demo av Link History Analyzer."""
    from pathlib import Path

    # Hitta databas
    db_path = Path(__file__).resolve().parents[2] / "data" / "output" / "linkops_history.db"

    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}")
        return

    # Analysera customer_id 117 (bethard.com)
    analyzer = LinkHistoryAnalyzer(str(db_path))
    analysis = analyzer.analyze_customer(117)

    if analysis:
        analyzer.print_analysis(analysis)
    else:
        print("No data found for customer 117")


if __name__ == "__main__":
    demo()

