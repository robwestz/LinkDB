# app/reset_history_db.py
from pathlib import Path

from settings import DB_PATH

if DB_PATH.exists():
    DB_PATH.unlink()
    print(f"🗑️  Tog bort {DB_PATH}")
else:
    print(f"ℹ️  Ingen fil att ta bort: {DB_PATH}")
