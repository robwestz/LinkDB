"""
Temporal Pattern Analyzer - Analyserar tidsmönster i länkbyggnad.

Denna modul analyserar:
- Länkhastighet över tid (velocity)
- Acceleration och deceleration
- Gaps och irregulariteter
- Säsongsmönster
- Spike detection (onaturliga toppar)
- Konsistens i länkbyggnad
"""

from __future__ import annotations

import math
import sqlite3
import statistics
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


@dataclass
class TemporalMetrics:
    """Temporala metrics för länkbyggnad."""

    customer_id: int
    canonical_root: str

    # Basic timeline
    total_links: int
    first_link_date: Optional[datetime]
    last_link_date: Optional[datetime]
    days_active: int
    total_months: int

    # Velocity metrics
    links_per_day: float
    links_per_week: float
    links_per_month: float

    # Acceleration
    velocity_trend: str  # increasing, decreasing, stable, irregular
    acceleration_score: float  # positive = accelerating, negative = decelerating

    # Consistency
    consistency_score: float  # 0-100, högre = mer konsistent
    coefficient_of_variation: float  # CV of monthly links
    longest_gap_days: int
    avg_gap_days: float

    # Monthly breakdown
    monthly_distribution: Dict[str, int]  # "YYYY-MM" -> count
    best_month: Tuple[str, int]  # (month, count)
    worst_month: Tuple[str, int]

    # Spike detection
    has_unnatural_spikes: bool
    spike_months: List[Tuple[str, int]]  # Months with suspicious spikes

    # Warnings & insights
    warnings: List[str]
    insights: List[str]
    health_score: float  # 0-100, overall temporal health


class TemporalPatternAnalyzer:
    """
    Analyserar tidsmönster i länkbyggnad.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path

    def analyze_customer(self, customer_id: int) -> Optional[TemporalMetrics]:
        """
        Analysera temporala mönster för en kund.
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

        # Hämta alla länkar med datum
        links = con.execute(
            """
            SELECT published_at, created_at
            FROM links_history
            WHERE customer_id = ?
            ORDER BY published_at, created_at
        """,
            (customer_id,),
        ).fetchall()

        con.close()

        if not links:
            return None

        # Parse dates
        dates = []
        for link in links:
            date_str = link["published_at"] or link["created_at"]
            if date_str:
                try:
                    if isinstance(date_str, str):
                        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                        # Remove timezone info for easier calculation
                        dt = dt.replace(tzinfo=None)
                        dates.append(dt)
                except:
                    pass

        if not dates:
            return None

        total_links = len(dates)
        first_date = min(dates)
        last_date = max(dates)
        days_active = (last_date - first_date).days + 1

        # Velocity
        links_per_day = total_links / days_active if days_active > 0 else 0
        links_per_week = links_per_day * 7
        links_per_month = links_per_day * 30

        # Monthly distribution
        monthly_dist = self._calculate_monthly_distribution(dates)
        total_months = len(monthly_dist)

        # Best/worst months
        if monthly_dist:
            best_month = max(monthly_dist.items(), key=lambda x: x[1])
            worst_month = min(monthly_dist.items(), key=lambda x: x[1])
        else:
            best_month = ("N/A", 0)
            worst_month = ("N/A", 0)

        # Velocity trend & acceleration
        velocity_trend, acceleration = self._analyze_velocity_trend(monthly_dist)

        # Consistency
        consistency_score, cv = self._calculate_consistency(monthly_dist)

        # Gaps
        longest_gap, avg_gap = self._analyze_gaps(dates)

        # Spike detection
        has_spikes, spike_months = self._detect_spikes(monthly_dist)

        # Warnings & insights
        warnings = self._generate_warnings(
            links_per_month, cv, longest_gap, has_spikes, velocity_trend
        )
        insights = self._generate_insights(
            monthly_dist, velocity_trend, consistency_score, best_month
        )

        # Health score
        health_score = self._calculate_health_score(
            consistency_score, has_spikes, cv, longest_gap, days_active
        )

        return TemporalMetrics(
            customer_id=customer_id,
            canonical_root=customer["canonical_root"],
            total_links=total_links,
            first_link_date=first_date,
            last_link_date=last_date,
            days_active=days_active,
            total_months=total_months,
            links_per_day=links_per_day,
            links_per_week=links_per_week,
            links_per_month=links_per_month,
            velocity_trend=velocity_trend,
            acceleration_score=acceleration,
            consistency_score=consistency_score,
            coefficient_of_variation=cv,
            longest_gap_days=longest_gap,
            avg_gap_days=avg_gap,
            monthly_distribution=monthly_dist,
            best_month=best_month,
            worst_month=worst_month,
            has_unnatural_spikes=has_spikes,
            spike_months=spike_months,
            warnings=warnings,
            insights=insights,
            health_score=health_score,
        )

    def _calculate_monthly_distribution(self, dates: List[datetime]) -> Dict[str, int]:
        """Gruppera länkar per månad."""
        monthly = defaultdict(int)
        for dt in dates:
            month_key = dt.strftime("%Y-%m")
            monthly[month_key] += 1
        return dict(monthly)

    def _analyze_velocity_trend(
        self, monthly_dist: Dict[str, int]
    ) -> Tuple[str, float]:
        """Analysera om velocity ökar, minskar eller är stabil."""
        if len(monthly_dist) < 3:
            return "insufficient_data", 0.0

        months_sorted = sorted(monthly_dist.items())
        counts = [count for _, count in months_sorted]

        # Simple linear regression slope
        n = len(counts)
        x = list(range(n))
        mean_x = sum(x) / n
        mean_y = sum(counts) / n

        numerator = sum((x[i] - mean_x) * (counts[i] - mean_y) for i in range(n))
        denominator = sum((x[i] - mean_x) ** 2 for i in range(n))

        if denominator == 0:
            slope = 0
        else:
            slope = numerator / denominator

        # Classify trend
        if abs(slope) < 0.5:
            trend = "stable"
        elif slope > 0:
            trend = "increasing"
        else:
            trend = "decreasing"

        return trend, slope

    def _calculate_consistency(
        self, monthly_dist: Dict[str, int]
    ) -> Tuple[float, float]:
        """
        Beräkna konsistens i länkbyggnad.
        Använder coefficient of variation (CV).
        """
        if len(monthly_dist) < 2:
            return 100.0, 0.0

        counts = list(monthly_dist.values())
        mean_count = statistics.mean(counts)

        if mean_count == 0:
            return 0.0, 0.0

        stdev = statistics.stdev(counts) if len(counts) > 1 else 0
        cv = stdev / mean_count

        # Convert CV to consistency score (lower CV = higher consistency)
        # CV of 0 = 100% consistency, CV of 2+ = low consistency
        consistency = max(0, 100 - (cv * 50))

        return consistency, cv

    def _analyze_gaps(self, dates: List[datetime]) -> Tuple[int, float]:
        """Analysera gaps mellan länkar."""
        if len(dates) < 2:
            return 0, 0.0

        sorted_dates = sorted(dates)
        gaps = []

        for i in range(1, len(sorted_dates)):
            gap_days = (sorted_dates[i] - sorted_dates[i - 1]).days
            gaps.append(gap_days)

        longest_gap = max(gaps) if gaps else 0
        avg_gap = sum(gaps) / len(gaps) if gaps else 0

        return longest_gap, avg_gap

    def _detect_spikes(
        self, monthly_dist: Dict[str, int]
    ) -> Tuple[bool, List[Tuple[str, int]]]:
        """
        Detektera onaturliga toppar i länkbyggnad.
        Använder statistisk outlier detection (Z-score method).
        """
        if len(monthly_dist) < 3:
            return False, []

        counts = list(monthly_dist.values())
        mean_count = statistics.mean(counts)

        if len(counts) < 2:
            return False, []

        stdev = statistics.stdev(counts)

        if stdev == 0:
            return False, []

        # Find outliers (Z-score > 2.5)
        spikes = []
        for month, count in monthly_dist.items():
            z_score = abs((count - mean_count) / stdev)
            if z_score > 2.5 and count > mean_count:
                spikes.append((month, count))

        has_spikes = len(spikes) > 0
        return has_spikes, sorted(spikes, key=lambda x: x[1], reverse=True)

    def _generate_warnings(
        self,
        links_per_month: float,
        cv: float,
        longest_gap: int,
        has_spikes: bool,
        velocity_trend: str,
    ) -> List[str]:
        """Generera varningar."""
        warnings = []

        if links_per_month > 50:
            warnings.append(
                f"⚠️ MYCKET HÖG HASTIGHET: {links_per_month:.1f} länkar/månad kan verka onaturligt"
            )
        elif links_per_month > 30:
            warnings.append(
                f"⚠️ Hög hastighet: {links_per_month:.1f} länkar/månad - säkerställ naturlighet"
            )

        if cv > 1.5:
            warnings.append(
                f"⚠️ Mycket inkonsistent länkbyggnad (CV: {cv:.2f}) - kan trigga algoritmer"
            )
        elif cv > 1.0:
            warnings.append(
                f"💡 Ganska inkonsistent länkbyggnad (CV: {cv:.2f}) - jämnare tempo rekommenderas"
            )

        if longest_gap > 90:
            warnings.append(
                f"⚠️ Längsta gap: {longest_gap} dagar - långa pauser kan skada momentum"
            )
        elif longest_gap > 60:
            warnings.append(
                f"💡 Längsta gap: {longest_gap} dagar - överväg mer konsekvent tempo"
            )

        if has_spikes:
            warnings.append(
                "⚠️ Onaturliga toppar detekterade - kan signalera manipulativ länkbyggnad"
            )

        if velocity_trend == "decreasing":
            warnings.append("📉 Vikande trend - länkhastigheten minskar över tid")

        if not warnings:
            warnings.append("✅ Temporalt mönster ser naturligt ut")

        return warnings

    def _generate_insights(
        self,
        monthly_dist: Dict[str, int],
        velocity_trend: str,
        consistency_score: float,
        best_month: Tuple[str, int],
    ) -> List[str]:
        """Generera insights."""
        insights = []

        if velocity_trend == "increasing":
            insights.append(
                "📈 Positiv trend: Länkbyggnaden accelererar över tid (bra för momentum)"
            )

        if consistency_score > 75:
            insights.append(
                f"✅ Utmärkt konsistens ({consistency_score:.1f}/100) - naturligt och hållbart tempo"
            )

        if len(monthly_dist) >= 6:
            recent_months = sorted(monthly_dist.items())[-3:]
            recent_avg = sum(count for _, count in recent_months) / len(recent_months)
            insights.append(
                f"📊 Senaste 3 månaderna: Genomsnitt {recent_avg:.1f} länkar/månad"
            )

        insights.append(f"🏆 Bästa månad: {best_month[0]} med {best_month[1]} länkar")

        return insights

    def _calculate_health_score(
        self,
        consistency: float,
        has_spikes: bool,
        cv: float,
        longest_gap: int,
        days_active: int,
    ) -> float:
        """Beräkna overall temporal health score."""
        score = 0.0

        # Consistency (40 points)
        score += consistency * 0.4

        # No spikes (20 points)
        if not has_spikes:
            score += 20

        # CV penalty (20 points)
        cv_score = max(0, 100 - (cv * 50))
        score += cv_score * 0.2

        # Gap penalty (10 points)
        if longest_gap < 30:
            score += 10
        elif longest_gap < 60:
            score += 7
        elif longest_gap < 90:
            score += 4

        # Activity duration bonus (10 points)
        if days_active > 180:
            score += 10
        elif days_active > 90:
            score += 7
        elif days_active > 30:
            score += 4

        return min(max(score, 0), 100)

    def print_analysis(self, metrics: TemporalMetrics):
        """Skriv ut snygg analys."""
        print("\n" + "=" * 70)
        print(f"TEMPORAL PATTERN ANALYSIS: {metrics.canonical_root}")
        print("=" * 70)

        print(f"\n📊 OVERVIEW")
        print(f"  Health Score: {metrics.health_score:.1f}/100")
        print(f"  Total links: {metrics.total_links}")
        print(
            f"  Active period: {metrics.days_active} days ({metrics.total_months} months)"
        )

        if metrics.first_link_date:
            print(f"\n📅 TIMELINE")
            print(f"  First link: {metrics.first_link_date.strftime('%Y-%m-%d')}")
            print(f"  Last link: {metrics.last_link_date.strftime('%Y-%m-%d')}")

        print(f"\n⚡ VELOCITY METRICS")
        print(f"  Links per day: {metrics.links_per_day:.2f}")
        print(f"  Links per week: {metrics.links_per_week:.1f}")
        print(f"  Links per month: {metrics.links_per_month:.1f}")
        print(f"  Trend: {metrics.velocity_trend.upper()}")
        print(f"  Acceleration: {metrics.acceleration_score:+.2f}")

        print(f"\n📈 CONSISTENCY")
        print(f"  Consistency Score: {metrics.consistency_score:.1f}/100")
        print(f"  Coefficient of Variation: {metrics.coefficient_of_variation:.2f}")
        print(f"  Longest gap: {metrics.longest_gap_days} days")
        print(f"  Average gap: {metrics.avg_gap_days:.1f} days")

        print(f"\n📊 MONTHLY PERFORMANCE")
        print(f"  Best month: {metrics.best_month[0]} ({metrics.best_month[1]} links)")
        print(
            f"  Worst month: {metrics.worst_month[0]} ({metrics.worst_month[1]} links)"
        )

        if metrics.has_unnatural_spikes:
            print(f"\n⚠️ SPIKE DETECTION")
            print(f"  Unnatural spikes detected: YES")
            for month, count in metrics.spike_months[:3]:
                print(f"    - {month}: {count} links (outlier)")
        else:
            print(f"\n✅ SPIKE DETECTION")
            print(f"  No unnatural spikes detected")

        print(f"\n⚠️ WARNINGS")
        for warning in metrics.warnings:
            print(f"  {warning}")

        print(f"\n💡 INSIGHTS")
        for insight in metrics.insights:
            print(f"  {insight}")

        # Monthly distribution chart
        if metrics.monthly_distribution:
            print(f"\n📊 MONTHLY DISTRIBUTION")
            max_count = max(metrics.monthly_distribution.values())
            for month in sorted(metrics.monthly_distribution.keys()):
                count = metrics.monthly_distribution[month]
                bar_length = int((count / max_count) * 40) if max_count > 0 else 0
                bar = "█" * bar_length
                print(f"  {month}: {bar} {count}")


def demo():
    """Demo av Temporal Pattern Analyzer."""
    from pathlib import Path

    db_path = (
        Path(__file__).resolve().parents[2] / "data" / "output" / "linkops_history.db"
    )

    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}")
        return

    analyzer = TemporalPatternAnalyzer(str(db_path))
    metrics = analyzer.analyze_customer(117)  # bethard.com

    if metrics:
        analyzer.print_analysis(metrics)
    else:
        print("No temporal data found")


if __name__ == "__main__":
    demo()
