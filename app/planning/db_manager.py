"""
Planning Database Manager - Hanterar planning-databasen och schema.
"""
from __future__ import annotations
import sqlite3
from pathlib import Path
from typing import Optional


class PlanningDBManager:
    """Manager för planning-databasen."""

    def __init__(self, db_path: str):
        """
        Initialize database manager.

        Args:
            db_path: Path to planning database
        """
        self.db_path = Path(db_path)
        self.schema_path = Path(__file__).parent / "schema_planning.sql"

    def initialize_database(self, force: bool = False):
        """
        Initialisera databasen med planning-schema.

        Args:
            force: Om True, droppa existerande tabeller först
        """
        if force and self.db_path.exists():
            print(f"Removing existing database: {self.db_path}")
            self.db_path.unlink()

        con = sqlite3.connect(self.db_path)

        # Läs schema
        if not self.schema_path.exists():
            raise FileNotFoundError(f"Schema file not found: {self.schema_path}")

        schema_sql = self.schema_path.read_text(encoding='utf-8')

        print(f"Initializing planning database: {self.db_path}")
        con.executescript(schema_sql)
        con.commit()
        con.close()

        print("✅ Planning database initialized successfully")

    def add_default_strategies(self):
        """Lägg till default planning strategies."""
        con = sqlite3.connect(self.db_path)

        strategies = [
            (
                "single_focus",
                "Fokusera på en starkt optimerad länk",
                1, 1,
                '{"exact": 50, "branded": 50}',
                0, 0, "high"
            ),
            (
                "diversified_basics",
                "Diversifiera ankartexter, grund för flera sidor",
                2, 5,
                '{"exact": 20, "partial": 30, "branded": 30, "generic": 20}',
                0, 0, "medium"
            ),
            (
                "semantic_foundation",
                "Börja bygga semantiska kluster, grundläggande authority",
                6, 15,
                '{"exact": 15, "partial": 35, "branded": 20, "generic": 20, "lsi": 10}',
                1, 1, "medium"
            ),
            (
                "topical_authority",
                "Full topical authority-strategi med flera kluster",
                16, 30,
                '{"exact": 10, "partial": 35, "branded": 20, "generic": 20, "lsi": 15}',
                1, 1, "low"
            ),
            (
                "enterprise_authority",
                "Enterprise-strategi med djup topic coverage",
                31, 9999,
                '{"exact": 8, "partial": 37, "branded": 20, "generic": 20, "lsi": 15}',
                1, 1, "low"
            ),
        ]

        con.executemany("""
            INSERT OR IGNORE INTO planning_strategies 
            (strategy_name, description, link_count_min, link_count_max, 
             anchor_distribution, semantic_clustering, topical_authority_focus, 
             diversification_level)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, strategies)

        con.commit()
        con.close()

        print(f"✅ Added {len(strategies)} default strategies")

    def get_table_counts(self) -> dict:
        """Hämta antal rader i varje tabell."""
        con = sqlite3.connect(self.db_path)
        cur = con.cursor()

        tables = [
            'link_plans', 'planned_links', 'semantic_clusters',
            'entities', 'related_phrases', 'customer_analysis',
            'planning_metrics', 'anchor_distribution', 'target_pages',
            'page_keywords', 'planning_strategies'
        ]

        counts = {}
        for table in tables:
            try:
                count = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
                counts[table] = count
            except sqlite3.OperationalError:
                counts[table] = "N/A"

        con.close()
        return counts

    def print_status(self):
        """Skriv ut status för databasen."""
        if not self.db_path.exists():
            print(f"❌ Database does not exist: {self.db_path}")
            return

        print(f"\n📊 Planning Database Status")
        print(f"Path: {self.db_path}")
        print(f"Size: {self.db_path.stat().st_size / 1024:.1f} KB")

        counts = self.get_table_counts()

        print(f"\nTable row counts:")
        for table, count in counts.items():
            print(f"  {table}: {count}")


def init_planning_db(db_path: Optional[str] = None, force: bool = False):
    """
    Initialisera planning-databasen.

    Args:
        db_path: Path till databas (default: linkops_planning.db i output/)
        force: Droppa och återskapa om den finns
    """
    if db_path is None:
        # Default location
        db_path = Path(__file__).resolve().parents[1] / "data" / "output" / "linkops_planning.db"

    manager = PlanningDBManager(str(db_path))

    print("\n" + "="*70)
    print("PLANNING DATABASE INITIALIZATION")
    print("="*70 + "\n")

    manager.initialize_database(force=force)
    manager.add_default_strategies()
    manager.print_status()

    print("\n✅ Planning database ready to use!")
    print("\n💡 Next steps:")
    print("  1. Run analyzers to analyze historical data")
    print("  2. Import planning document from Google Sheets")
    print("  3. Generate link plans")


if __name__ == "__main__":
    import sys

    force = "--force" in sys.argv or "-f" in sys.argv

    init_planning_db(force=force)

