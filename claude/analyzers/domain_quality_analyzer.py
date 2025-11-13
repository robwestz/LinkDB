"""
Domain Quality Analyzer - Analyserar kvaliteten på publiceringsdomenerna.

Denna modul analyserar:
- Domain diversity och distribution
- TLD distribution (för geografisk och kvalitetsinsikt)
- Domain concentration risk
- Cross-linking patterns
- New vs returning domains
- Domain authority indicators (baserat på patterns)
"""

from __future__ import annotations

import sqlite3
from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional, Set, Tuple

import tldextract


@dataclass
class DomainQualityMetrics:
    """Kvalitetsmått för publishing domains."""

    customer_id: int
    canonical_root: str

    # Basic metrics
    total_links: int
    unique_domains: int
    domain_diversity_score: float  # 0-100

    # Distribution
    tld_distribution: Dict[str, int]  # .com, .se, etc
    top_tlds: List[Tuple[str, int]]

    # Concentration
    top_domain_concentration: float  # % of links from top domain
    top_5_concentration: float  # % of links from top 5 domains
    gini_coefficient: float  # 0-1, inequality measure

    # Domain behavior
    single_link_domains: int  # Domains with only 1 link
    multi_link_domains: int  # Domains with 2+ links
    power_domains: List[Tuple[str, int]]  # Domains with 5+ links

    # Cross-linking detection
    potential_pbn_domains: List[str]  # Domains appearing too often
    cross_linking_score: float  # 0-100, higher = more suspicious

    # Geographic distribution
    geographic_diversity: Dict[str, int]  # Country code -> count
    is_geo_diverse: bool

    # Quality indicators
    quality_score: float  # 0-100, overall domain quality
    warnings: List[str]
    insights: List[str]

    # Top domains
    top_domains: List[Tuple[str, int]]  # (domain, link_count)


class DomainQualityAnalyzer:
    """
    Analyserar kvaliteten på domains som länkar till kunden.
    """

    # Geographic TLD mapping (simplified)
    GEO_TLDS = {
        "se": "Sweden",
        "no": "Norway",
        "dk": "Denmark",
        "fi": "Finland",
        "de": "Germany",
        "uk": "United Kingdom",
        "fr": "France",
        "es": "Spain",
        "it": "Italy",
        "nl": "Netherlands",
        "io": "International",
        "com": "Commercial",
        "org": "Organization",
        "net": "Network",
    }

    def __init__(self, db_path: str):
        self.db_path = db_path

    def analyze_customer(self, customer_id: int) -> Optional[DomainQualityMetrics]:
        """
        Analysera domain kvalitet för en kund.
        """
        con = sqlite3.connect(self.db_path)
        con.row_factory = sqlite3.Row

        # Hämta customer info
        customer = con.execute(
            "SELECT canonical_root FROM customers WHERE id = ?", (customer_id,)
        ).fetchone()

        if not customer:
            con.close()
            return None

        # Hämta alla publishing domains
        links = con.execute(
            """
            SELECT pub_domain
            FROM links_history
            WHERE customer_id = ? AND pub_domain IS NOT NULL AND TRIM(pub_domain) <> ''
        """,
            (customer_id,),
        ).fetchall()

        con.close()

        if not links:
            return None

        domains = [link["pub_domain"] for link in links]
        total_links = len(domains)
        unique_domains = len(set(domains))

        # Domain counter
        domain_counter = Counter(domains)
        top_domains = domain_counter.most_common(20)

        # Diversity score
        diversity_score = min((unique_domains / total_links) * 100, 100)

        # TLD analysis
        tld_dist, top_tlds = self._analyze_tlds(domains)

        # Concentration
        top_domain_conc = (
            (domain_counter.most_common(1)[0][1] / total_links) if domain_counter else 0
        )
        top_5_count = sum(count for _, count in domain_counter.most_common(5))
        top_5_conc = top_5_count / total_links

        gini = self._calculate_gini_coefficient(list(domain_counter.values()))

        # Domain behavior
        single_link = sum(1 for count in domain_counter.values() if count == 1)
        multi_link = sum(1 for count in domain_counter.values() if count >= 2)
        power_doms = [
            (dom, count) for dom, count in domain_counter.items() if count >= 5
        ]

        # Cross-linking / PBN detection
        potential_pbn, cross_link_score = self._detect_suspicious_patterns(
            domain_counter, total_links, unique_domains
        )

        # Geographic diversity
        geo_dist = self._analyze_geographic_diversity(domains)
        is_geo_diverse = len(geo_dist) >= 3

        # Quality score
        quality_score = self._calculate_quality_score(
            diversity_score,
            top_domain_conc,
            gini,
            cross_link_score,
            single_link,
            unique_domains,
        )

        # Warnings & insights
        warnings = self._generate_warnings(
            top_domain_conc,
            top_5_conc,
            cross_link_score,
            single_link,
            unique_domains,
            potential_pbn,
        )

        insights = self._generate_insights(
            diversity_score, geo_dist, power_doms, is_geo_diverse
        )

        return DomainQualityMetrics(
            customer_id=customer_id,
            canonical_root=customer["canonical_root"],
            total_links=total_links,
            unique_domains=unique_domains,
            domain_diversity_score=diversity_score,
            tld_distribution=tld_dist,
            top_tlds=top_tlds,
            top_domain_concentration=top_domain_conc,
            top_5_concentration=top_5_conc,
            gini_coefficient=gini,
            single_link_domains=single_link,
            multi_link_domains=multi_link,
            power_domains=power_doms,
            potential_pbn_domains=potential_pbn,
            cross_linking_score=cross_link_score,
            geographic_diversity=geo_dist,
            is_geo_diverse=is_geo_diverse,
            quality_score=quality_score,
            warnings=warnings,
            insights=insights,
            top_domains=top_domains,
        )

    def _analyze_tlds(
        self, domains: List[str]
    ) -> Tuple[Dict[str, int], List[Tuple[str, int]]]:
        """Analysera TLD distribution."""
        tld_counter = Counter()

        for domain in domains:
            extracted = tldextract.extract(domain)
            tld = extracted.suffix or "unknown"
            tld_counter[tld] += 1

        tld_dist = dict(tld_counter)
        top_tlds = tld_counter.most_common(10)

        return tld_dist, top_tlds

    def _calculate_gini_coefficient(self, values: List[int]) -> float:
        """Beräkna Gini coefficient för ojämnhet."""
        if not values:
            return 0.0

        sorted_values = sorted(values)
        n = len(sorted_values)
        cumsum = 0

        for i, val in enumerate(sorted_values):
            cumsum += (i + 1) * val

        return (2 * cumsum) / (n * sum(sorted_values)) - (n + 1) / n

    def _detect_suspicious_patterns(
        self, domain_counter: Counter, total_links: int, unique_domains: int
    ) -> Tuple[List[str], float]:
        """
        Detektera misstänkta PBN-mönster.

        Red flags:
        - En domain med >30% av alla länkar
        - Flera domains med samma mönster (kan indikera PBN)
        """
        suspicious = []
        score = 0.0

        # Check top domain dominance
        if domain_counter:
            top_domain, top_count = domain_counter.most_common(1)[0]
            top_ratio = top_count / total_links

            if top_ratio > 0.3:
                suspicious.append(top_domain)
                score += 40

            # Check if multiple domains have suspiciously high counts
            high_count_domains = [
                dom
                for dom, count in domain_counter.items()
                if count > max(5, total_links * 0.15)
            ]

            if len(high_count_domains) > 1:
                suspicious.extend(high_count_domains[1:])
                score += 20 * len(high_count_domains)

        # Low diversity also suspicious
        if unique_domains < 10 and total_links > 20:
            score += 30

        return suspicious[:5], min(score, 100)

    def _analyze_geographic_diversity(self, domains: List[str]) -> Dict[str, int]:
        """Analysera geografisk spridning baserat på TLD."""
        geo_counter = Counter()

        for domain in domains:
            extracted = tldextract.extract(domain)
            tld = extracted.suffix

            if tld in self.GEO_TLDS:
                country = self.GEO_TLDS[tld]
                geo_counter[country] += 1
            else:
                geo_counter["Other"] += 1

        return dict(geo_counter)

    def _calculate_quality_score(
        self,
        diversity: float,
        top_conc: float,
        gini: float,
        cross_link_score: float,
        single_link_count: int,
        unique_domains: int,
    ) -> float:
        """Beräkna overall quality score."""
        score = 0.0

        # Diversity (30 points)
        score += diversity * 0.3

        # Low concentration is good (20 points)
        concentration_score = (1 - top_conc) * 100
        score += concentration_score * 0.2

        # Low gini is good (15 points)
        gini_score = (1 - gini) * 100
        score += gini_score * 0.15

        # Low cross-linking risk (20 points)
        cross_link_penalty = cross_link_score * 0.2
        score += max(0, 20 - cross_link_penalty)

        # Good domain diversity (15 points)
        if unique_domains >= 20:
            score += 15
        elif unique_domains >= 10:
            score += 10
        elif unique_domains >= 5:
            score += 5

        return min(max(score, 0), 100)

    def _generate_warnings(
        self,
        top_conc: float,
        top_5_conc: float,
        cross_link_score: float,
        single_link_count: int,
        unique_domains: int,
        potential_pbn: List[str],
    ) -> List[str]:
        """Generera varningar."""
        warnings = []

        if top_conc > 0.5:
            warnings.append(
                f"⚠️ KRITISK: {top_conc*100:.1f}% av länkar kommer från EN domain - mycket riskabelt"
            )
        elif top_conc > 0.3:
            warnings.append(
                f"⚠️ {top_conc*100:.1f}% av länkar från top domain - för koncentrerat"
            )

        if top_5_conc > 0.7:
            warnings.append(
                f"⚠️ {top_5_conc*100:.1f}% av länkar från bara 5 domäner - diversifiera mer"
            )

        if cross_link_score > 60:
            warnings.append(
                f"⚠️ HÖG PBN-RISK: Cross-linking score {cross_link_score:.0f}/100"
            )
        elif cross_link_score > 30:
            warnings.append(
                f"💡 Potentiell PBN-aktivitet detekterad (score: {cross_link_score:.0f}/100)"
            )

        if potential_pbn:
            warnings.append(f"⚠️ Misstänkta domäner: {', '.join(potential_pbn[:3])}")

        if unique_domains < 5 and len(warnings) == 0:
            warnings.append(
                f"💡 Endast {unique_domains} unika domäner - öka diversifieringen"
            )

        if not warnings:
            warnings.append("✅ Domain profil ser naturlig och varierad ut")

        return warnings

    def _generate_insights(
        self,
        diversity: float,
        geo_dist: Dict[str, int],
        power_domains: List[Tuple[str, int]],
        is_geo_diverse: bool,
    ) -> List[str]:
        """Generera insights."""
        insights = []

        if diversity > 75:
            insights.append(f"✅ Utmärkt domain diversity ({diversity:.1f}/100)")

        if is_geo_diverse:
            top_geos = sorted(geo_dist.items(), key=lambda x: x[1], reverse=True)[:3]
            geo_str = ", ".join(f"{geo} ({count})" for geo, count in top_geos)
            insights.append(f"🌍 Geografisk spridning: {geo_str}")

        if power_domains:
            insights.append(
                f"💪 {len(power_domains)} 'power domains' (5+ länkar) ger stark foundation"
            )

        return insights

    def print_analysis(self, metrics: DomainQualityMetrics):
        """Skriv ut snygg analys."""
        print("\n" + "=" * 70)
        print(f"DOMAIN QUALITY ANALYSIS: {metrics.canonical_root}")
        print("=" * 70)

        print(f"\n📊 OVERVIEW")
        print(f"  Quality Score: {metrics.quality_score:.1f}/100")
        print(f"  Total links: {metrics.total_links}")
        print(f"  Unique domains: {metrics.unique_domains}")
        print(f"  Diversity Score: {metrics.domain_diversity_score:.1f}/100")

        print(f"\n📈 CONCENTRATION ANALYSIS")
        print(f"  Top domain: {metrics.top_domain_concentration*100:.1f}% of links")
        print(f"  Top 5 domains: {metrics.top_5_concentration*100:.1f}% of links")
        print(f"  Gini coefficient: {metrics.gini_coefficient:.3f}")

        print(f"\n🔗 DOMAIN BEHAVIOR")
        print(f"  Single-link domains: {metrics.single_link_domains}")
        print(f"  Multi-link domains: {metrics.multi_link_domains}")
        print(f"  Power domains (5+): {len(metrics.power_domains)}")

        if metrics.cross_linking_score > 0:
            print(f"\n⚠️ RISK ASSESSMENT")
            print(f"  Cross-linking score: {metrics.cross_linking_score:.0f}/100")
            if metrics.potential_pbn_domains:
                print(
                    f"  Suspicious domains detected: {len(metrics.potential_pbn_domains)}"
                )

        print(f"\n🌍 GEOGRAPHIC DIVERSITY")
        print(f"  Is geo-diverse: {'YES' if metrics.is_geo_diverse else 'NO'}")
        if metrics.geographic_diversity:
            for geo, count in sorted(
                metrics.geographic_diversity.items(), key=lambda x: x[1], reverse=True
            )[:5]:
                print(f"    - {geo}: {count} links")

        if metrics.top_tlds:
            print(f"\n🏷️ TOP TLDs")
            for tld, count in metrics.top_tlds[:8]:
                pct = (count / metrics.total_links) * 100
                print(f"  .{tld}: {count} ({pct:.1f}%)")

        print(f"\n⚠️ WARNINGS")
        for warning in metrics.warnings:
            print(f"  {warning}")

        print(f"\n💡 INSIGHTS")
        for insight in metrics.insights:
            print(f"  {insight}")

        if metrics.top_domains:
            print(f"\n🔝 TOP 10 DOMAINS")
            for i, (domain, count) in enumerate(metrics.top_domains[:10], 1):
                pct = (count / metrics.total_links) * 100
                print(f"  {i}. {domain} ({count} links, {pct:.1f}%)")


def demo():
    """Demo av Domain Quality Analyzer."""
    from pathlib import Path

    db_path = (
        Path(__file__).resolve().parents[2] / "data" / "output" / "linkops_history.db"
    )

    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}")
        return

    analyzer = DomainQualityAnalyzer(str(db_path))
    metrics = analyzer.analyze_customer(117)  # bethard.com

    if metrics:
        analyzer.print_analysis(metrics)
    else:
        print("No domain data found")


if __name__ == "__main__":
    demo()
