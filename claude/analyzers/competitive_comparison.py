"""
Competitive Comparison - Jämför kunder mot varandra för benchmarking.

Detta verktyg låter dig:
- Identifiera top performers
- Hitta best practices
- Benchmarka mot branschgenomsnitt
- Identifiera gap och förbättringsområden
"""

from __future__ import annotations

import sqlite3
import statistics
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class CustomerBenchmark:
    """Benchmark data för en kund."""

    customer_id: int
    canonical_root: str
    brand: str

    # Volume metrics
    total_links: int
    unique_domains: int
    unique_target_urls: int
    links_per_month: float

    # Quality scores (from analyzers)
    anchor_diversity: float
    domain_diversity: float
    consistency_score: float

    # Rankings
    volume_percentile: float  # 0-100
    quality_percentile: float  # 0-100
    overall_percentile: float  # 0-100


@dataclass
class CompetitiveInsights:
    """Competitive insights och benchmarks."""

    total_customers_analyzed: int

    # Industry benchmarks
    avg_total_links: float
    median_total_links: float
    avg_links_per_month: float
    avg_anchor_diversity: float
    avg_domain_diversity: float

    # Top performers
    top_10_by_volume: List[Tuple[str, int]]  # (domain, links)
    top_10_by_quality: List[Tuple[str, float]]  # (domain, quality_score)
    top_10_by_diversity: List[Tuple[str, float]]  # (domain, diversity)

    # Distribution
    volume_distribution: Dict[str, int]  # "0-10", "11-25", etc
    quality_tiers: Dict[str, int]  # "poor", "fair", "good", "excellent"


class CompetitiveComparison:
    """
    Jämför kunder mot varandra för competitive benchmarking.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

    def analyze_all_customers(self) -> CompetitiveInsights:
        """
        Analysera alla kunder och skapa benchmarks.
        """
        con = sqlite3.connect(self.db_path)
        con.row_factory = sqlite3.Row

        # Get all customers with links
        customers = con.execute(
            """
            SELECT c.id, c.canonical_root, c.brand,
                   COUNT(l.id) as total_links,
                   COUNT(DISTINCT l.pub_domain) as unique_domains,
                   COUNT(DISTINCT l.target_url) as unique_target_urls,
                   COUNT(DISTINCT l.anchor_text) as unique_anchors
            FROM customers c
            LEFT JOIN links_history l ON c.id = l.customer_id
            GROUP BY c.id
            HAVING total_links > 0
        """
        ).fetchall()

        con.close()

        if not customers:
            return None

        # Collect metrics
        all_link_counts = []
        all_domain_counts = []
        benchmarks = []

        for cust in customers:
            total_links = cust["total_links"]
            unique_domains = cust["unique_domains"]
            unique_target_urls = cust["unique_target_urls"]
            unique_anchors = cust["unique_anchors"]

            all_link_counts.append(total_links)
            all_domain_counts.append(unique_domains)

            # Calculate diversity scores
            anchor_diversity = (
                min((unique_anchors / total_links) * 100, 100) if total_links > 0 else 0
            )
            domain_diversity = (
                min((unique_domains / total_links) * 100, 100) if total_links > 0 else 0
            )

            # Simplified consistency (would need temporal data for real calculation)
            consistency_score = 70.0  # Placeholder

            benchmarks.append(
                {
                    "customer_id": cust["id"],
                    "canonical_root": cust["canonical_root"],
                    "brand": cust["brand"] or cust["canonical_root"],
                    "total_links": total_links,
                    "unique_domains": unique_domains,
                    "unique_target_urls": unique_target_urls,
                    "anchor_diversity": anchor_diversity,
                    "domain_diversity": domain_diversity,
                    "consistency_score": consistency_score,
                    "quality_score": (anchor_diversity + domain_diversity) / 2,
                }
            )

        # Calculate industry benchmarks
        avg_links = statistics.mean(all_link_counts)
        median_links = statistics.median(all_link_counts)
        avg_anchor_div = statistics.mean(b["anchor_diversity"] for b in benchmarks)
        avg_domain_div = statistics.mean(b["domain_diversity"] for b in benchmarks)

        # Top performers
        top_by_volume = sorted(
            benchmarks, key=lambda x: x["total_links"], reverse=True
        )[:10]
        top_by_quality = sorted(
            benchmarks, key=lambda x: x["quality_score"], reverse=True
        )[:10]
        top_by_diversity = sorted(
            benchmarks, key=lambda x: x["domain_diversity"], reverse=True
        )[:10]

        top_volume_list = [
            (b["canonical_root"], b["total_links"]) for b in top_by_volume
        ]
        top_quality_list = [
            (b["canonical_root"], b["quality_score"]) for b in top_by_quality
        ]
        top_diversity_list = [
            (b["canonical_root"], b["domain_diversity"]) for b in top_by_diversity
        ]

        # Volume distribution
        volume_dist = {
            "0-10": sum(1 for x in all_link_counts if 0 <= x <= 10),
            "11-25": sum(1 for x in all_link_counts if 11 <= x <= 25),
            "26-50": sum(1 for x in all_link_counts if 26 <= x <= 50),
            "51-100": sum(1 for x in all_link_counts if 51 <= x <= 100),
            "100+": sum(1 for x in all_link_counts if x > 100),
        }

        # Quality tiers
        quality_tiers = {
            "poor (0-40)": sum(1 for b in benchmarks if b["quality_score"] < 40),
            "fair (40-60)": sum(1 for b in benchmarks if 40 <= b["quality_score"] < 60),
            "good (60-80)": sum(1 for b in benchmarks if 60 <= b["quality_score"] < 80),
            "excellent (80-100)": sum(
                1 for b in benchmarks if b["quality_score"] >= 80
            ),
        }

        return CompetitiveInsights(
            total_customers_analyzed=len(customers),
            avg_total_links=avg_links,
            median_total_links=median_links,
            avg_links_per_month=avg_links / 6,  # Rough estimate
            avg_anchor_diversity=avg_anchor_div,
            avg_domain_diversity=avg_domain_div,
            top_10_by_volume=top_volume_list,
            top_10_by_quality=top_quality_list,
            top_10_by_diversity=top_diversity_list,
            volume_distribution=volume_dist,
            quality_tiers=quality_tiers,
        )

    def compare_customer(self, customer_id: int) -> Optional[Dict]:
        """
        Jämför en specifik kund mot alla andra.
        """
        insights = self.analyze_all_customers()
        if not insights:
            return None

        con = sqlite3.connect(self.db_path)
        con.row_factory = sqlite3.Row

        # Get customer data
        cust = con.execute(
            """
            SELECT c.id, c.canonical_root, c.brand,
                   COUNT(l.id) as total_links,
                   COUNT(DISTINCT l.pub_domain) as unique_domains,
                   COUNT(DISTINCT l.target_url) as unique_target_urls,
                   COUNT(DISTINCT l.anchor_text) as unique_anchors
            FROM customers c
            LEFT JOIN links_history l ON c.id = l.customer_id
            WHERE c.id = ?
            GROUP BY c.id
        """,
            (customer_id,),
        ).fetchone()

        con.close()

        if not cust:
            return None

        total_links = cust["total_links"]
        unique_anchors = cust["unique_anchors"]
        unique_domains = cust["unique_domains"]

        anchor_div = (
            min((unique_anchors / total_links) * 100, 100) if total_links > 0 else 0
        )
        domain_div = (
            min((unique_domains / total_links) * 100, 100) if total_links > 0 else 0
        )

        # Calculate percentiles
        volume_percentile = self._calculate_percentile(
            total_links, insights.avg_total_links
        )
        quality_score = (anchor_div + domain_div) / 2
        quality_percentile = self._calculate_percentile(
            quality_score,
            (insights.avg_anchor_diversity + insights.avg_domain_diversity) / 2,
        )

        return {
            "customer": cust["canonical_root"],
            "total_links": total_links,
            "unique_domains": unique_domains,
            "anchor_diversity": anchor_div,
            "domain_diversity": domain_div,
            "volume_percentile": volume_percentile,
            "quality_percentile": quality_percentile,
            "vs_avg_links": total_links - insights.avg_total_links,
            "vs_median_links": total_links - insights.median_total_links,
            "insights": insights,
        }

    def _calculate_percentile(self, value: float, avg: float) -> float:
        """Simple percentile calculation."""
        if avg == 0:
            return 50.0
        ratio = value / avg
        percentile = min(max((ratio * 50), 0), 100)
        return percentile

    def print_competitive_insights(self, insights: CompetitiveInsights):
        """Print competitive insights."""
        print("\n" + "=" * 70)
        print("COMPETITIVE BENCHMARKING ANALYSIS")
        print("=" * 70)

        print(f"\n📊 INDUSTRY OVERVIEW")
        print(f"  Total customers analyzed: {insights.total_customers_analyzed}")
        print(f"  Average links per customer: {insights.avg_total_links:.1f}")
        print(f"  Median links per customer: {insights.median_total_links:.0f}")
        print(f"  Average links per month: {insights.avg_links_per_month:.1f}")

        print(f"\n📈 QUALITY BENCHMARKS")
        print(f"  Average anchor diversity: {insights.avg_anchor_diversity:.1f}%")
        print(f"  Average domain diversity: {insights.avg_domain_diversity:.1f}%")

        print(f"\n🏆 TOP 10 BY VOLUME")
        for i, (domain, links) in enumerate(insights.top_10_by_volume, 1):
            print(f"  {i}. {domain}: {links} links")

        print(f"\n⭐ TOP 10 BY QUALITY")
        for i, (domain, quality) in enumerate(insights.top_10_by_quality, 1):
            print(f"  {i}. {domain}: {quality:.1f} quality score")

        print(f"\n📊 VOLUME DISTRIBUTION")
        for range_name, count in insights.volume_distribution.items():
            pct = (count / insights.total_customers_analyzed) * 100
            bar = "█" * int(pct / 2)
            print(f"  {range_name:10s}: {bar} {count} ({pct:.1f}%)")

        print(f"\n🎯 QUALITY TIERS")
        for tier, count in insights.quality_tiers.items():
            pct = (count / insights.total_customers_analyzed) * 100
            bar = "█" * int(pct / 2)
            print(f"  {tier:20s}: {bar} {count} ({pct:.1f}%)")

    def print_customer_comparison(self, comparison: Dict):
        """Print customer vs industry comparison."""
        print("\n" + "=" * 70)
        print(f"CUSTOMER BENCHMARKING: {comparison['customer']}")
        print("=" * 70)

        print(f"\n📊 YOUR METRICS")
        print(f"  Total links: {comparison['total_links']}")
        print(f"  Unique domains: {comparison['unique_domains']}")
        print(f"  Anchor diversity: {comparison['anchor_diversity']:.1f}%")
        print(f"  Domain diversity: {comparison['domain_diversity']:.1f}%")

        print(f"\n📈 VS INDUSTRY")
        avg_diff = comparison["vs_avg_links"]
        median_diff = comparison["vs_median_links"]

        print(
            f"  Volume vs average: {avg_diff:+.1f} links ({'above' if avg_diff > 0 else 'below'} average)"
        )
        print(
            f"  Volume vs median: {median_diff:+.0f} links ({'above' if median_diff > 0 else 'below'} median)"
        )
        print(f"  Volume percentile: {comparison['volume_percentile']:.0f}th")
        print(f"  Quality percentile: {comparison['quality_percentile']:.0f}th")

        print(f"\n💡 COMPETITIVE POSITION")
        if comparison["volume_percentile"] >= 75:
            print(f"  📈 VOLUME: Top 25% - You're outperforming most competitors")
        elif comparison["volume_percentile"] >= 50:
            print(f"  📊 VOLUME: Above average - Solid performance")
        else:
            print(f"  📉 VOLUME: Below average - Room for growth")

        if comparison["quality_percentile"] >= 75:
            print(f"  ⭐ QUALITY: Top 25% - Excellent link profile quality")
        elif comparison["quality_percentile"] >= 50:
            print(f"  ✓ QUALITY: Above average - Good quality profile")
        else:
            print(f"  ⚠️ QUALITY: Below average - Focus on quality improvement")


def demo():
    """Demo av Competitive Comparison."""
    from pathlib import Path

    db_path = (
        Path(__file__).resolve().parents[2] / "data" / "output" / "linkops_history.db"
    )

    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}")
        return

    comp = CompetitiveComparison(str(db_path))

    # Industry insights
    insights = comp.analyze_all_customers()
    if insights:
        comp.print_competitive_insights(insights)

    # Customer comparison
    comparison = comp.compare_customer(117)  # bethard.com
    if comparison:
        comp.print_customer_comparison(comparison)


if __name__ == "__main__":
    demo()
