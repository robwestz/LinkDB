#!/usr/bin/env python3
"""
Database migration tool for LinkDB.

Applies SQL migrations to the database in order.
"""

import sqlite3
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from config import get_database_path
from logging_config import logger


def get_applied_migrations(conn):
    """Get list of already applied migrations."""
    cursor = conn.cursor()

    # Create migrations table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS _migrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()

    # Get applied migrations
    cursor.execute("SELECT name FROM _migrations ORDER BY id")
    return [row[0] for row in cursor.fetchall()]


def apply_migration(conn, migration_file):
    """Apply a single migration file."""
    cursor = conn.cursor()

    migration_name = migration_file.name

    logger.info(f"Applying migration: {migration_name}")

    # Read and execute migration SQL
    with open(migration_file, 'r') as f:
        sql = f.read()

    try:
        # Execute all statements in the migration
        cursor.executescript(sql)

        # Record migration as applied
        cursor.execute(
            "INSERT INTO _migrations (name) VALUES (?)",
            (migration_name,)
        )

        conn.commit()
        logger.info(f"✅ Migration applied successfully: {migration_name}")
        return True

    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Migration failed: {migration_name}", exc_info=True)
        raise


def run_migrations():
    """Run all pending migrations."""
    try:
        # Get database path
        db_path = get_database_path()

        if not db_path.exists():
            logger.error(f"Database not found: {db_path}")
            return False

        logger.info(f"Connecting to database: {db_path}")

        # Connect to database
        conn = sqlite3.connect(str(db_path))

        # Get applied migrations
        applied = get_applied_migrations(conn)
        logger.info(f"Already applied migrations: {len(applied)}")

        # Get all migration files
        migrations_dir = Path(__file__).parent
        migration_files = sorted(migrations_dir.glob("*.sql"))

        if not migration_files:
            logger.info("No migration files found")
            return True

        logger.info(f"Found {len(migration_files)} migration file(s)")

        # Apply pending migrations
        pending = [f for f in migration_files if f.name not in applied]

        if not pending:
            logger.info("✅ All migrations already applied")
            return True

        logger.info(f"Applying {len(pending)} pending migration(s)...")

        for migration_file in pending:
            apply_migration(conn, migration_file)

        conn.close()

        logger.info(f"✅ All migrations completed successfully")
        return True

    except Exception as e:
        logger.error("❌ Migration process failed", exc_info=True)
        return False


if __name__ == "__main__":
    success = run_migrations()
    sys.exit(0 if success else 1)
