"""
Anchor Quality Analyzer - Djupgående analys av anchor text kvalitet och naturlighet.

Denna modul analyserar:
- Anchor text diversity (Shannon entropy)
- Anchor naturlighet (flaggar över-optimering)
- Anchor text längd och komplexitet
- Brand vs commercial ratio
- Semantic clustering av anchors
"""

from __future__ import annotations

import math
import re
import sqlite3
from collections import Counter
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class AnchorQualityMetrics:
    """Kvalitetsmått för anchor text profil."""

    customer_id: int
    canonical_root: str

    # Diversity metrics
    total_anchors: int
    unique_anchors: int
    shannon_entropy: float  # 0-inf, högre = mer diverse
    diversity_score: float  # 0-100, normalized score

    # Length & complexity
    avg_anchor_length: float  # chars
    avg_word_count: float
    min_length: int
    max_length: int

    # Naturlighet
    over_optimization_risk: str  # low, medium, high
    exact_match_ratio: float  # 0-1
    branded_ratio: float  # 0-1
    commercial_keywords_ratio: float  # 0-1

    # Distribution insights
    anchor_type_distribution: Dict[str, float]  # type -> percentage
    top_10_concentration: float  # % av länkar i top 10 anchors
    gini_coefficient: float  # 0-1, inequality measure (0=perfect equality)

    # Red flags & warnings
    warnings: List[str]
    quality_score: float  # 0-100, overall quality

    # Details
    top_anchors: List[Tuple[str, int]]  # (anchor, count)
    single_use_anchors: int  # anchors used only once


class AnchorQualityAnalyzer:
    """
    Analyserar kvalitet och naturlighet i anchor text profilen.
    """

    COMMERCIAL_KEYWORDS = {
        "köp",
        "buy",
        "bäst",
        "best",
        "billig",
        "cheap",
        "gratis",
        "free",
        "erbjudande",
        "deals",
        "rabatt",
        "discount",
        "casino",
        "betting",
        "spela",
        "play",
        "vinn",
        "win",
        "bonus",
        "odds",
    }

    def __init__(self, db_path: str):
        self.db_path = db_path

    def analyze_customer(self, customer_id: int) -> Optional[AnchorQualityMetrics]:
        """
        Analysera anchor text kvalitet för en kund.
        """
        con = sqlite3.connect(self.db_path)
        con.row_factory = sqlite3.Row

        # Hämta customer info
        customer = con.execute(
            "SELECT canonical_root, brand FROM customers WHERE id = ?", (customer_id,)
        ).fetchone()

        if not customer:
            con.close()
            return None

        # Hämta alla anchors
        anchors_raw = con.execute(
            """
            SELECT anchor_text, anchor_type
            FROM links_history
            WHERE customer_id = ? AND anchor_text IS NOT NULL AND TRIM(anchor_text) <> ''
        """,
            (customer_id,),
        ).fetchall()

        con.close()

        if not anchors_raw:
            return None

        anchors = [row["anchor_text"] for row in anchors_raw]
        anchor_types = [row["anchor_type"] for row in anchors_raw if row["anchor_type"]]
        brand = customer["brand"] or customer["canonical_root"]

        # Räkna och analysera
        total_anchors = len(anchors)
        unique_anchors = len(set(anchors))
        anchor_counter = Counter(anchors)

        # Shannon entropy
        shannon_entropy = self._calculate_shannon_entropy(anchor_counter, total_anchors)
        diversity_score = min(shannon_entropy / math.log2(total_anchors) * 100, 100)

        # Length & complexity
        lengths = [len(a) for a in anchors]
        word_counts = [len(a.split()) for a in anchors]
        avg_length = sum(lengths) / len(lengths)
        avg_words = sum(word_counts) / len(word_counts)

        # Naturlighet
        exact_match_count = sum(1 for wc in word_counts if wc <= 2)
        exact_match_ratio = exact_match_count / total_anchors

        branded_count = sum(1 for a in anchors if self._is_branded(a, brand))
        branded_ratio = branded_count / total_anchors

        commercial_count = sum(1 for a in anchors if self._has_commercial_keywords(a))
        commercial_ratio = commercial_count / total_anchors

        # Over-optimization risk
        over_opt_risk = self._assess_over_optimization_risk(
            exact_match_ratio, commercial_ratio, diversity_score
        )

        # Distribution
        anchor_type_dist = self._calculate_type_distribution(
            anchor_types, total_anchors
        )
        top_10_anchors = anchor_counter.most_common(10)
        top_10_count = sum(count for _, count in top_10_anchors)
        top_10_concentration = top_10_count / total_anchors

        # Gini coefficient (inequality)
        gini = self._calculate_gini_coefficient(list(anchor_counter.values()))

        # Single use anchors
        single_use = sum(1 for count in anchor_counter.values() if count == 1)

        # Warnings & quality score
        warnings = self._generate_warnings(
            exact_match_ratio,
            commercial_ratio,
            diversity_score,
            top_10_concentration,
            gini,
            branded_ratio,
        )

        quality_score = self._calculate_quality_score(
            diversity_score,
            over_opt_risk,
            top_10_concentration,
            gini,
            branded_ratio,
            commercial_ratio,
        )

        return AnchorQualityMetrics(
            customer_id=customer_id,
            canonical_root=customer["canonical_root"],
            total_anchors=total_anchors,
            unique_anchors=unique_anchors,
            shannon_entropy=shannon_entropy,
            diversity_score=diversity_score,
            avg_anchor_length=avg_length,
            avg_word_count=avg_words,
            min_length=min(lengths),
            max_length=max(lengths),
            over_optimization_risk=over_opt_risk,
            exact_match_ratio=exact_match_ratio,
            branded_ratio=branded_ratio,
            commercial_keywords_ratio=commercial_ratio,
            anchor_type_distribution=anchor_type_dist,
            top_10_concentration=top_10_concentration,
            gini_coefficient=gini,
            warnings=warnings,
            quality_score=quality_score,
            top_anchors=top_10_anchors,
            single_use_anchors=single_use,
        )

    def _calculate_shannon_entropy(self, counter: Counter, total: int) -> float:
        """Shannon entropy measure för diversity."""
        entropy = 0.0
        for count in counter.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)
        return entropy

    def _is_branded(self, anchor: str, brand: str) -> bool:
        """Kollar om anchor innehåller brand name."""
        if not brand:
            return False
        return brand.lower() in anchor.lower()

    def _has_commercial_keywords(self, anchor: str) -> bool:
        """Kollar om anchor innehåller kommersiella keywords."""
        anchor_lower = anchor.lower()
        return any(kw in anchor_lower for kw in self.COMMERCIAL_KEYWORDS)

    def _assess_over_optimization_risk(
        self, exact_ratio: float, commercial_ratio: float, diversity: float
    ) -> str:
        """Bedöm risk för över-optimering."""
        risk_score = 0

        if exact_ratio > 0.5:
            risk_score += 2
        elif exact_ratio > 0.3:
            risk_score += 1

        if commercial_ratio > 0.6:
            risk_score += 2
        elif commercial_ratio > 0.4:
            risk_score += 1

        if diversity < 30:
            risk_score += 2
        elif diversity < 50:
            risk_score += 1

        if risk_score >= 4:
            return "high"
        elif risk_score >= 2:
            return "medium"
        return "low"

    def _calculate_type_distribution(
        self, anchor_types: List[str], total: int
    ) -> Dict[str, float]:
        """Beräkna distribution av anchor types."""
        if not anchor_types:
            return {}

        type_counter = Counter(anchor_types)
        return {atype: (count / total) * 100 for atype, count in type_counter.items()}

    def _calculate_gini_coefficient(self, values: List[int]) -> float:
        """
        Beräkna Gini coefficient för ojämnhet i distribution.
        0 = perfekt jämn distribution
        1 = maximal ojämnhet
        """
        if not values:
            return 0.0

        sorted_values = sorted(values)
        n = len(sorted_values)
        cumsum = 0

        for i, val in enumerate(sorted_values):
            cumsum += (i + 1) * val

        return (2 * cumsum) / (n * sum(sorted_values)) - (n + 1) / n

    def _generate_warnings(
        self,
        exact_ratio: float,
        commercial_ratio: float,
        diversity: float,
        top10_conc: float,
        gini: float,
        branded_ratio: float,
    ) -> List[str]:
        """Generera varningar baserat på metrics."""
        warnings = []

        if exact_ratio > 0.4:
            warnings.append(
                f"⚠️ HOOG RISK: {exact_ratio*100:.1f}% exact match anchors - Google kan flagga detta"
            )

        if commercial_ratio > 0.6:
            warnings.append(
                f"⚠️ För många kommersiella keywords ({commercial_ratio*100:.1f}%) - minska aggressiviteten"
            )

        if diversity < 30:
            warnings.append(
                f"⚠️ Mycket låg diversity ({diversity:.1f}/100) - varierar anchor texts mer"
            )

        if top10_conc > 0.7:
            warnings.append(
                f"⚠️ {top10_conc*100:.1f}% av länkar använder samma 10 anchors - för repetitivt"
            )

        if gini > 0.8:
            warnings.append(
                "⚠️ Mycket ojämn distribution - några anchors dominerar för mycket"
            )

        if branded_ratio < 0.1:
            warnings.append("💡 Överväg fler branded anchors för naturlighet")

        if not warnings:
            warnings.append("✅ Anchor profil ser naturlig och balanserad ut")

        return warnings

    def _calculate_quality_score(
        self,
        diversity: float,
        over_opt_risk: str,
        top10_conc: float,
        gini: float,
        branded_ratio: float,
        commercial_ratio: float,
    ) -> float:
        """Beräkna overall quality score 0-100."""
        score = 0.0

        # Diversity (40 points)
        score += diversity * 0.4

        # Over-optimization (20 points)
        if over_opt_risk == "low":
            score += 20
        elif over_opt_risk == "medium":
            score += 10

        # Distribution (20 points)
        distribution_score = (1 - top10_conc) * 100 + (1 - gini) * 100
        score += (distribution_score / 2) * 0.2

        # Naturlighet (20 points)
        natural_score = 100
        if branded_ratio < 0.05:
            natural_score -= 30
        elif branded_ratio < 0.15:
            natural_score -= 15

        if commercial_ratio > 0.6:
            natural_score -= 30
        elif commercial_ratio > 0.4:
            natural_score -= 15

        score += natural_score * 0.2

        return min(max(score, 0), 100)

    def print_analysis(self, metrics: AnchorQualityMetrics):
        """Skriv ut snygg analys."""
        print("\n" + "=" * 70)
        print(f"ANCHOR QUALITY ANALYSIS: {metrics.canonical_root}")
        print("=" * 70)

        print(f"\n📊 OVERVIEW")
        print(f"  Quality Score: {metrics.quality_score:.1f}/100")
        print(f"  Over-optimization Risk: {metrics.over_optimization_risk.upper()}")
        print(f"  Total anchors: {metrics.total_anchors}")
        print(f"  Unique anchors: {metrics.unique_anchors}")
        print(f"  Single-use anchors: {metrics.single_use_anchors}")

        print(f"\n📈 DIVERSITY METRICS")
        print(f"  Shannon Entropy: {metrics.shannon_entropy:.2f}")
        print(f"  Diversity Score: {metrics.diversity_score:.1f}/100")
        print(
            f"  Gini Coefficient: {metrics.gini_coefficient:.3f} (0=equal, 1=unequal)"
        )
        print(f"  Top 10 Concentration: {metrics.top_10_concentration*100:.1f}%")

        print(f"\n📏 LENGTH & COMPLEXITY")
        print(f"  Avg anchor length: {metrics.avg_anchor_length:.1f} chars")
        print(f"  Avg word count: {metrics.avg_word_count:.1f} words")
        print(f"  Range: {metrics.min_length}-{metrics.max_length} chars")

        print(f"\n🎯 NATURLIGHET")
        print(f"  Exact match ratio: {metrics.exact_match_ratio*100:.1f}%")
        print(f"  Branded ratio: {metrics.branded_ratio*100:.1f}%")
        print(f"  Commercial keywords: {metrics.commercial_keywords_ratio*100:.1f}%")

        if metrics.anchor_type_distribution:
            print(f"\n🏷️ ANCHOR TYPE DISTRIBUTION")
            for atype, pct in sorted(
                metrics.anchor_type_distribution.items(),
                key=lambda x: x[1],
                reverse=True,
            ):
                print(f"  {atype}: {pct:.1f}%")

        print(f"\n⚠️ WARNINGS & RECOMMENDATIONS")
        for warning in metrics.warnings:
            print(f"  {warning}")

        if metrics.top_anchors:
            print(f"\n🔝 TOP 10 ANCHORS")
            for i, (anchor, count) in enumerate(metrics.top_anchors, 1):
                pct = (count / metrics.total_anchors) * 100
                print(f'  {i}. "{anchor}" ({count}x, {pct:.1f}%)')


def demo():
    """Demo av Anchor Quality Analyzer."""
    from pathlib import Path

    db_path = (
        Path(__file__).resolve().parents[2] / "data" / "output" / "linkops_history.db"
    )

    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}")
        return

    analyzer = AnchorQualityAnalyzer(str(db_path))
    metrics = analyzer.analyze_customer(117)  # bethard.com

    if metrics:
        analyzer.print_analysis(metrics)
    else:
        print("No anchor data found")


if __name__ == "__main__":
    demo()
