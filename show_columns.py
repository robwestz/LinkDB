from pathlib import Path
import pandas as pd

INPUT_XLSX = Path("data/input/main_sheet.xlsx")
print(f"📄 Fil: {INPUT_XLSX.resolve()}")
df = pd.read_excel(INPUT_XLSX, engine="openpyxl")  # tvinga engine
print("\n✅ Upptäckta kolumner:")
for c in df.columns:
    print(f"- {repr(c)}")
