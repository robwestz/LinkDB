from pathlib import Path

# Filvägar
DATA_DIR = Path(__file__).resolve().parents[1] / "data"
INPUT_XLSX = DATA_DIR / "input" / "main_sheet.xlsx"
DB_PATH = DATA_DIR / "output" / "linkops_history.db"

# Kolumnnamn i main_sheet.xlsx
COLUMNS = {
    "canonical_root": "canonical_root",
    "pub_page_url": "pub_page_url",
    "target_url": "target_url",
    "anchor_text": "anchor_text",
    "brand": "brand",
    "link_type": "link_type",
    "language": "language",
    "published_at": "published_at",
}

# Frivilliga (läggs till om de finns i arket)
OPTIONAL = ["topic_tags", "context_excerpt", "anchor_type"]
