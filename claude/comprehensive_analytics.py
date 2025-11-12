"""
Comprehensive Analytics - Kör alla analyser för en kund.

Detta script kombinerar alla analysmoduler för att ge en komplett bild:
- Link History Analysis
- Anchor Quality Analysis
- Temporal Pattern Analysis
- Domain Quality Analysis
"""
from pathlib import Path
import sys
import io

# Fix Windows console encoding for emojis
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Add app directory to path
app_dir = Path(__file__).parent / "app"
sys.path.insert(0, str(app_dir))

from analyzers.link_history_analyzer import LinkHistoryAnalyzer
from analyzers.anchor_quality_analyzer import AnchorQualityAnalyzer
from analyzers.temporal_pattern_analyzer import TemporalPatternAnalyzer
from analyzers.domain_quality_analyzer import DomainQualityAnalyzer


class ComprehensiveAnalytics:
    """
    Kör alla analyser för en kund och presenterar en unified rapport.
    """

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.history_analyzer = LinkHistoryAnalyzer(db_path)
        self.anchor_analyzer = AnchorQualityAnalyzer(db_path)
        self.temporal_analyzer = TemporalPatternAnalyzer(db_path)
        self.domain_analyzer = DomainQualityAnalyzer(db_path)

    def analyze_customer(self, customer_id: int):
        """
        Kör alla analyser för en kund.
        """
        print("\n" + "="*80)
        print("COMPREHENSIVE BACKLINK ANALYTICS")
        print("="*80)
        print(f"\nAnalyzing Customer ID: {customer_id}")
        print("Running all analysis modules...\n")

        # Run all analyses
        history = self.history_analyzer.analyze_customer(customer_id)
        anchor = self.anchor_analyzer.analyze_customer(customer_id)
        temporal = self.temporal_analyzer.analyze_customer(customer_id)
        domain = self.domain_analyzer.analyze_customer(customer_id)

        # Print results
        if history:
            self.history_analyzer.print_analysis(history)
        else:
            print("❌ No historical data found")

        if anchor:
            self.anchor_analyzer.print_analysis(anchor)
        else:
            print("❌ No anchor data found")

        if temporal:
            self.temporal_analyzer.print_analysis(temporal)
        else:
            print("❌ No temporal data found")

        if domain:
            self.domain_analyzer.print_analysis(domain)
        else:
            print("❌ No domain data found")

        # Print executive summary
        self._print_executive_summary(history, anchor, temporal, domain)

    def _print_executive_summary(self, history, anchor, temporal, domain):
        """Print en executive summary med key metrics."""
        print("\n" + "="*80)
        print("EXECUTIVE SUMMARY")
        print("="*80)

        if not any([history, anchor, temporal, domain]):
            print("\nNo data available for analysis.")
            return

        print("\n📊 KEY PERFORMANCE INDICATORS")

        if history:
            print(f"\n  Link Portfolio:")
            print(f"    • Total links: {history.total_links}")
            print(f"    • Unique domains: {history.unique_pub_domains}")
            print(f"    • Target URLs: {history.unique_target_urls}")
            print(f"    • Strategy: {history.primary_strategy}")

        if anchor:
            print(f"\n  Anchor Text Quality:")
            print(f"    • Quality Score: {anchor.quality_score:.1f}/100")
            print(f"    • Diversity Score: {anchor.diversity_score:.1f}/100")
            print(f"    • Over-optimization Risk: {anchor.over_optimization_risk.upper()}")

        if temporal:
            print(f"\n  Temporal Health:")
            print(f"    • Health Score: {temporal.health_score:.1f}/100")
            print(f"    • Velocity: {temporal.links_per_month:.1f} links/month")
            print(f"    • Trend: {temporal.velocity_trend.upper()}")
            print(f"    • Consistency: {temporal.consistency_score:.1f}/100")

        if domain:
            print(f"\n  Domain Quality:")
            print(f"    • Quality Score: {domain.quality_score:.1f}/100")
            print(f"    • Unique domains: {domain.unique_domains}")
            print(f"    • Diversity: {domain.domain_diversity_score:.1f}/100")
            print(f"    • PBN Risk Score: {domain.cross_linking_score:.0f}/100")

        # Overall health assessment
        print(f"\n🎯 OVERALL HEALTH ASSESSMENT")

        scores = []
        if anchor:
            scores.append(anchor.quality_score)
        if temporal:
            scores.append(temporal.health_score)
        if domain:
            scores.append(domain.quality_score)

        if scores:
            overall_score = sum(scores) / len(scores)
            print(f"  Overall Score: {overall_score:.1f}/100")

            if overall_score >= 80:
                assessment = "EXCELLENT - Very healthy backlink profile"
            elif overall_score >= 60:
                assessment = "GOOD - Solid foundation with room for improvement"
            elif overall_score >= 40:
                assessment = "FAIR - Needs attention in several areas"
            else:
                assessment = "POOR - Significant risks and issues detected"

            print(f"  Assessment: {assessment}")

        # Prioritized recommendations
        print(f"\n💡 TOP 3 PRIORITY RECOMMENDATIONS")

        all_warnings = []
        if history:
            all_warnings.extend([(w, 'Strategy') for w in history.recommendations if '⚠️' in w])
        if anchor:
            all_warnings.extend([(w, 'Anchor') for w in anchor.warnings if '⚠️' in w])
        if temporal:
            all_warnings.extend([(w, 'Temporal') for w in temporal.warnings if '⚠️' in w])
        if domain:
            all_warnings.extend([(w, 'Domain') for w in domain.warnings if '⚠️' in w])

        if all_warnings:
            for i, (warning, category) in enumerate(all_warnings[:3], 1):
                print(f"  {i}. [{category}] {warning}")
        else:
            print("  ✅ No critical issues detected!")

        print("\n" + "="*80 + "\n")


def main():
    """Main function."""
    # Find database
    db_path = Path(__file__).parent / "data" / "output" / "linkops_history.db"

    if not db_path.exists():
        print(f"ERROR: Database not found at {db_path}")
        return

    # Check command line arguments
    if len(sys.argv) > 1:
        try:
            customer_id = int(sys.argv[1])
        except ValueError:
            print("ERROR: Customer ID must be an integer")
            return
    else:
        # Default to customer 117 (bethard.com) for demo
        customer_id = 117
        print("No customer ID specified, using demo customer 117 (bethard.com)")

    # Run comprehensive analytics
    analytics = ComprehensiveAnalytics(str(db_path))
    analytics.analyze_customer(customer_id)


if __name__ == "__main__":
    main()
