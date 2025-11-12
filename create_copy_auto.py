"""
Automatisk projektkopia - kör med standardvärden
"""
from datetime import datetime
from pathlib import Path
import subprocess

# Skapa standardnamn
project_name = f"linkdb_dev_{datetime.now().strftime('%Y%m%d')}"

# Kör Python-skriptet med piped input
script_path = Path(__file__).parent / "create_project_copy.py"

# Simulera user input: tryck enter för standard, sedan 'y' för att fortsätta
process = subprocess.Popen(
    ["python", str(script_path)],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)

# Skicka input: enter för standardnamn, 'y' för bekräftelse
output, error = process.communicate(input=f"\ny\n")

print(output)
if error:
    print(error)

# Visa var kopian skapades
parent_dir = Path(__file__).parent.parent
new_project = parent_dir / project_name
print(f"\n✅ Kopia skapad: {new_project}")

