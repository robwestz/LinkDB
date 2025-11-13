"""
Initialize Planning System - Setup och demo av planeringssystemet
"""

import sys
from pathlib import Path

# Lägg till app i path
sys.path.insert(0, str(Path(__file__).parent))

from app.analyzers.link_history_analyzer import LinkHistoryAnalyzer
from app.planning.customer_grouper import CustomerGrouper
from app.planning.db_manager import init_planning_db


def main():
    """Huvudfunktion för att initialisera och demonstrera systemet."""

    print(
        """
╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║        INTELLIGENT LINK PLANNING SYSTEM - INITIALIZATION        ║
║                                                                  ║
║  Ett AI-drivet system för semantisk länkplanering baserat       ║
║  på topical authority och historisk länkdata.                   ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
    """
    )

    print("\n🚀 Starting initialization...\n")

    # Steg 1: Initiera planning database
    print("STEP 1: Initialize Planning Database")
    print("-" * 70)

    db_path = Path(__file__).parent / "data" / "output" / "linkops_planning.db"

    try:
        init_planning_db(str(db_path), force=False)
    except Exception as e:
        print(f"Error initializing database: {e}")
        return

    # Steg 2: Demonstrera Customer Grouper
    print("\n\nSTEP 2: Customer Grouping Demo")
    print("-" * 70)

    history_db = Path(__file__).parent / "data" / "output" / "linkops_history.db"

    if not history_db.exists():
        print(f"⚠️  History database not found: {history_db}")
        print("   Skipping customer grouping demo")
    else:
        print("\nGrouping customers by link volume...\n")

        # Exempel: Simulera counts från planeringsdokument
        sample_counts = {
            117: 15,  # bethard.com
            # I verkligheten skulle detta komma från Google Sheets
        }

        grouper = CustomerGrouper(str(history_db))
        groups = grouper.group_customers(sample_counts)
        grouper.print_summary(groups)

    # Steg 3: Demonstrera Link History Analyzer
    print("\n\nSTEP 3: Link History Analysis Demo")
    print("-" * 70)

    if history_db.exists():
        print("\nAnalyzing customer 117 (bethard.com)...\n")

        analyzer = LinkHistoryAnalyzer(str(history_db))
        analysis = analyzer.analyze_customer(117)

        if analysis:
            analyzer.print_analysis(analysis)
        else:
            print("No historical data found for customer 117")
    else:
        print("⚠️  History database not found, skipping analysis")

    # Sammanfattning
    print("\n\n" + "=" * 70)
    print("INITIALIZATION COMPLETE")
    print("=" * 70)

    print("\n✅ Planning system foundation is ready!")

    print("\n📚 What's been created:")
    print("  • Planning database with schema")
    print("  • Default planning strategies")
    print("  • Customer grouping module")
    print("  • Link history analyzer")

    print("\n🔜 Next steps (Fas 1 completion):")
    print("  [ ] Implement Google Sheets integration")
    print("  [ ] Import planning document")
    print("  [ ] Analyze all customers in planning doc")
    print("  [ ] Generate first simple plans")

    print("\n🔮 Future phases:")
    print("  Fas 2: Semantic SEO Engine")
    print("  Fas 3: Full automation & Intelligence")

    print("\n💡 To generate plans:")
    print("  python app/planning/plan_generator.py")

    print("\n📖 Documentation:")
    print(f"  See: {Path(__file__).parent / 'PLANNING_SYSTEM_SPEC.md'}")

    print("\n")


if __name__ == "__main__":
    main()
