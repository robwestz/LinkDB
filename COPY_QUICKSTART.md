# 🚀 Snabbguide: Kopiera projekt

## Skapa kopia (2 sätt)

### 1️⃣ Enklast - Dubbelklicka
```
create_copy.bat
```

### 2️⃣ Kommandorad
```bash
python create_project_copy.py
```

## Efter kopiering - 4 enkla steg

### 1. Gå till den nya mappen
```bash
cd ..\linkdb_dev_20250205
```

### 2. Kör setup (dubbelklicka eller kör i terminal)
```bash
setup_dev_environment.bat
```

### 3. Aktivera miljön
```bash
.venv\Scripts\activate
```

### 4. Testa att det fungerar
```bash
python show_columns.py
```

✅ Klart! Nu kan du utveckla fritt!

## Vad kopieras?

### ✅ Kopieras:
- All Python-kod
- Alla databaser (.db)
- Excel-filer och data
- Dokumentation
- Scripts

### ❌ Exkluderas:
- .venv (virtuell miljö)
- __pycache__ (cache)
- .git (versionshistorik)
- .idea/.vscode (IDE)
- Temporära filer

## Vanliga kommandon

```bash
# Skapa kopia
python create_project_copy.py

# Gå till kopian
cd ..\linkdb_dev_20250205

# Setup
setup_dev_environment.bat

# Aktivera (varje session)
.venv\Scripts\activate

# Testa
python show_columns.py

# Exportera data
python export_to_airtable_csv.py

# Bygg databaser
python app\build_all_customer_dbs.py
```

## Tips

💡 **Flera kopior:** Du kan ha flera kopior samtidigt med olika namn
```
linkdb_dev_20250205
linkdb_experiment_api
linkdb_test_new_feature
```

💡 **Synka tillbaka:** När något fungerar i kopian - kopiera tillbaka till original
```bash
copy export_to_airtable_csv.py ..\linkdb\
```

💡 **Namnge smart:** Använd beskrivande namn för att hålla reda på vad varje kopia är till för

## Problemlösning

❌ **"Python not found"**
→ Kontrollera att Python är installerat

❌ **Setup misslyckas**
→ Kör manuellt:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install rich openpyxl tldextract
```

❌ **Import errors**
→ Aktivera miljön: `.venv\Scripts\activate`

## Läs mer

- `GUIDE_PROJECT_COPY.md` - Detaljerad guide
- `README_COPY.md` - Finns i varje kopia

