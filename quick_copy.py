"""
Snabb projektkopia - ingen interaktion
"""
from __future__ import annotations
import shutil
from pathlib import Path
from datetime import datetime

# Konfiguration
CURRENT_PROJECT = Path(r"C:\Users\robin\PycharmProjects\linkdb")
parent_dir = CURRENT_PROJECT.parent
project_name = f"linkdb_dev_{datetime.now().strftime('%Y%m%d_%H%M')}"
destination = parent_dir / project_name

# Exkludera
EXCLUDE_PATTERNS = [
    '__pycache__', '*.pyc', '*.pyo', '*.pyd', '.pytest_cache',
    '.venv', 'venv', 'env', '.env', '.git', '.idea', '.vscode',
    '*.db-wal', '*.db-shm', 'node_modules', '.DS_Store', 'Thumbs.db',
]

def should_exclude(path: Path) -> bool:
    """Kontrollera om en fil/mapp ska exkluderas."""
    path_str = str(path)
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith('*.'):
            if path.suffix == pattern[1:]:
                return True
        else:
            if pattern in path_str or pattern == path.name:
                return True
    return False

print(f"Kopierar från: {CURRENT_PROJECT}")
print(f"Till: {destination}")
print()

# Skapa destination
destination.mkdir(parents=True, exist_ok=True)

copied = 0
skipped = 0

# Kopiera filer
for item in CURRENT_PROJECT.rglob('*'):
    if should_exclude(item):
        skipped += 1
        continue
    
    try:
        rel_path = item.relative_to(CURRENT_PROJECT)
        dest_path = destination / rel_path
        
        if item.is_dir():
            dest_path.mkdir(parents=True, exist_ok=True)
        else:
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest_path)
            copied += 1
            if copied % 50 == 0:
                print(f"Kopierat {copied} filer...")
    except Exception as e:
        print(f"Varning: {item.name}: {e}")

print()
print(f"✅ Klart!")
print(f"   Kopierade: {copied} filer")
print(f"   Överhoppade: {skipped} filer/mappar")
print()
print(f"📁 Kopia skapad: {destination}")
print()

# Skapa README
readme_content = f"""# LinkDB - Utvecklingskopia

Kopierad från: {CURRENT_PROJECT}
Skapad: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Setup

```bash
# Skapa virtuell miljö
python -m venv .venv
.venv\\Scripts\\activate

# Installera dependencies
pip install rich openpyxl tldextract

# Testa
python show_columns.py
```

Original: {CURRENT_PROJECT}
"""

(destination / "README_COPY.md").write_text(readme_content, encoding='utf-8')

# Skapa setup-script
setup_content = """@echo off
echo Skapar virtuell miljö...
python -m venv .venv
call .venv\\Scripts\\activate.bat
echo Installerar dependencies...
pip install --upgrade pip
pip install rich openpyxl tldextract
echo Klart!
pause
"""

(destination / "setup_dev_environment.bat").write_text(setup_content, encoding='utf-8')

print("📝 Skapade extra filer:")
print("   - README_COPY.md")
print("   - setup_dev_environment.bat")
print()
print("🚀 Nästa steg:")
print(f"   cd {destination}")
print("   setup_dev_environment.bat")

