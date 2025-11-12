# LinkDB - Komplett översikt

Detta projekt innehåller verktyg för att hantera kunddatabaser och exportera data till Airtable.

## 📁 Projektstruktur

```
linkdb/
├── app/                                    # Kärnfunktionalitet
│   ├── build_all_customer_dbs.py          # Bygg alla kunddatabaser
│   ├── build_history_db.py                # Bygg historikdatabas
│   ├── history_repo.py                    # Repository för historikdata
│   ├── reset_history_db.py                # Återställ historikdatabas
│   ├── schema.sql                         # Databasschema
│   └── settings.py                        # Projektinställningar
│
├── data/                                   # Data och databaser
│   ├── input/
│   │   └── main_sheet.xlsx                # Input Excel-fil
│   └── output/
│       ├── linkops_history.db             # Huvuddatabas
│       ├── customers/                     # Individuella kunddatabaser
│       └── airtable_export/               # Exporterade CSV-filer
│
├── build_customer_db.py                   # Bygg enskild kunddatabas
├── show_columns.py                        # Visa kolumner i Excel
│
├── export_to_airtable_csv.py             # ⭐ Exportera till Airtable (enkel)
├── export_advanced.py                     # ⭐ Avancerad export med filter
├── run_export.bat                         # Kör enkel export
│
├── create_project_copy.py                 # 🔒 Skapa säker projektkopia
├── create_copy.bat                        # Kör kopieringsverktyg
│
└── Dokumentation/
    ├── EXPORT_README.md                   # Guide för Airtable-export
    ├── SNABBGUIDE_EXPORT.md              # Snabbguide export
    ├── GUIDE_PROJECT_COPY.md             # Guide för projektkopia
    └── COPY_QUICKSTART.md                # Snabbguide kopia
```

## 🚀 Snabbstart

### 1. Exportera till Airtable (alla kunder)
```bash
python export_to_airtable_csv.py
```
eller dubbelklicka på `run_export.bat`

### 2. Avancerad export (välj kunder)
```bash
python export_advanced.py
```

### 3. Skapa säker kopia för utveckling
```bash
python create_project_copy.py
```
eller dubbelklicka på `create_copy.bat`

### 4. Bygg alla kunddatabaser
```bash
python app/build_all_customer_dbs.py
```

### 5. Bygg historikdatabas från Excel
```bash
python app/build_history_db.py
```

## 📚 Huvudfunktioner

### 🎯 Export till Airtable

**Enkel export (alla kunder):**
- Fil: `export_to_airtable_csv.py`
- Exporterar alla kunder och deras data
- Skapar 4 CSV-filer: customers, links, priority_pages, summary
- Output: `data/output/airtable_export/`

**Avancerad export (med filter):**
- Fil: `export_advanced.py`
- Interaktivt läge eller kommandoradsargument
- Filtrera per kund, brand eller domän
- Exportera endast specifika kunder

**Exempel:**
```bash
# Lista alla kunder
python export_advanced.py --list

# Exportera kunder 1-50
python export_advanced.py --customers "1-50"

# Exportera alla .se-domäner
python export_advanced.py --domain ".se"

# Exportera specifikt brand
python export_advanced.py --brand "Happy Socks"
```

### 🔒 Projektkopia (säker utveckling)

**Syfte:** Skapa en fullständig kopia av projektet för att utveckla nya funktioner utan risk

**Verktyg:**
- Fil: `create_project_copy.py`
- Batch: `create_copy.bat`

**Vad som händer:**
1. ✅ Kopierar all kod och databaser
2. ❌ Exkluderar .venv, cache, IDE-filer
3. 📝 Skapar README_COPY.md i kopian
4. 🔧 Skapar setup_dev_environment.bat för automatisk setup

**Efter kopiering:**
```bash
cd ..\linkdb_dev_20250205
setup_dev_environment.bat
.venv\Scripts\activate
python show_columns.py  # Testa att allt fungerar
```

### 🗄️ Databashantering

**Bygg historikdatabas från Excel:**
```bash
python app/build_history_db.py
```
- Läser: `data/input/main_sheet.xlsx`
- Skapar: `data/output/linkops_history.db`

**Bygg alla kunddatabaser:**
```bash
python app/build_all_customer_dbs.py
```
- Läser: `data/output/linkops_history.db`
- Skapar: En databas per kund i `data/output/customers/`

**Återställ historikdatabas:**
```bash
python app/reset_history_db.py
```

## 📖 Dokumentation

### Export-dokumentation
- **EXPORT_README.md** - Fullständig guide för Airtable-export
- **SNABBGUIDE_EXPORT.md** - Snabbreferens för export

### Kopia-dokumentation
- **GUIDE_PROJECT_COPY.md** - Fullständig guide för projektkopia
- **COPY_QUICKSTART.md** - Snabbreferens för kopiering

## 🛠️ Installation & Setup

### Förutsättningar
- Python 3.8 eller senare
- Virtuell miljö (rekommenderas)

### Installation
```bash
# Skapa virtuell miljö
python -m venv .venv

# Aktivera miljön
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Installera dependencies
pip install rich openpyxl tldextract
```

## 💡 Vanliga användningsfall

### Use Case 1: Exportera all data till Airtable
```bash
python export_to_airtable_csv.py
# → Öppna Airtable och importera CSV-filerna
```

### Use Case 2: Exportera endast vissa kunder
```bash
python export_advanced.py --customers "1,5,10-20"
```

### Use Case 3: Utveckla ny funktion
```bash
# 1. Skapa kopia
python create_project_copy.py

# 2. Gå till kopian
cd ..\linkdb_dev_20250205

# 3. Setup
setup_dev_environment.bat

# 4. Utveckla!
.venv\Scripts\activate
# ... din utveckling ...

# 5. Kopiera tillbaka när det fungerar
copy ny_funktion.py ..\linkdb\
```

### Use Case 4: Uppdatera databaser från ny Excel
```bash
# 1. Lägg ny main_sheet.xlsx i data/input/
# 2. Bygg om historikdatabas
python app/build_history_db.py

# 3. Bygg om alla kunddatabaser
python app/build_all_customer_dbs.py

# 4. Exportera till Airtable
python export_to_airtable_csv.py
```

## 🔍 Felsökning

### Problem: Import errors
**Lösning:** Aktivera virtuell miljö
```bash
.venv\Scripts\activate
```

### Problem: "No module named 'rich'"
**Lösning:** Installera dependencies
```bash
pip install rich openpyxl tldextract
```

### Problem: "Database is locked"
**Lösning:** Stäng alla program som använder databasen

### Problem: Excel-fil hittas inte
**Lösning:** Kontrollera att `data/input/main_sheet.xlsx` finns

### Problem: Svenska tecken ser konstiga ut
**Lösning:** Alla CSV-filer använder UTF-8 med BOM, vilket fungerar i Airtable

## 📊 Databasschema

### Huvuddatabas (linkops_history.db)
```sql
customers (id, canonical_root, brand, created_at)
links_history (id, customer_id, pub_page_url, target_url, anchor_text, ...)
```

### Kunddatabaser (customers/*/customer.db)
```sql
customers (id, canonical_root, brand, created_at)
links_history (id, customer_id, pub_page_url, target_url, anchor_text, ...)
priority_pages (id, url, priority_score, intent, keywords)
```

## 🎯 Bästa praxis

### Innan stora ändringar
1. Skapa en projektkopia: `python create_project_copy.py`
2. Testa ändringar i kopian
3. Kopiera tillbaka när det fungerar

### Backup av databaser
```bash
# Manuell backup
copy data\output\linkops_history.db data\output\linkops_history_backup_20250205.db
```

### Regelbunden export till Airtable
```bash
# Sätt upp scheduled task i Windows
# Kör: python export_to_airtable_csv.py
# Schema: Dagligen / Veckovis
```

## 🤝 Bidra

När du utvecklar nya funktioner:
1. Skapa projektkopia
2. Utveckla och testa
3. Dokumentera ändringar
4. Kopiera tillbaka till original
5. Uppdatera denna README om nödvändigt

## 📞 Support

Vid problem, kontrollera:
1. ✅ Python 3.8+ är installerat
2. ✅ Virtuell miljö är aktiverad
3. ✅ Dependencies är installerade
4. ✅ Databaser finns i rätt mappar
5. ✅ Excel-fil finns i data/input/

## 📝 Changelog

### 2025-01-05
- ✅ Skapat export till Airtable (enkel och avancerad)
- ✅ Skapat säker projektkopia-funktion
- ✅ Komplett dokumentation

---

**Tips:** Börja alltid med att läsa snabbguiderna för en snabb överblick!
- `SNABBGUIDE_EXPORT.md` för export
- `COPY_QUICKSTART.md` för projektkopia

