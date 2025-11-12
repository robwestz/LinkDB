├── export_to_airtable_csv.py
├── export_advanced.py
└── ...
```

## Användningsscenarier

### Scenario 1: Testa ny funktion
```bash
# Skapa kopia
python create_project_copy.py

# Gå till kopian
cd ..\linkdb_dev_20250205

# Setup
setup_dev_environment.bat

# Utveckla!
.venv\Scripts\activate
# ... gör dina ändringar ...
python test_ny_funktion.py
```

### Scenario 2: Experimentera med databaser
```bash
# Kopian har ALLA databaser
# Du kan ändra/ta bort/testa fritt
# Originalet påverkas inte
```

### Scenario 3: Stora refaktoreringar
```bash
# Skapa kopia för refaktoreringen
# Testa grundligt i kopian
# När allt fungerar - kopiera tillbaka koden till originalet
```

## Synkronisera ändringar tillbaka

När du har utvecklat något som fungerar i kopian:

### Manuell metod:
1. Kopiera de ändrade filerna från kopian
2. Klistra in dem i originalprojektet
3. Testa i originalprojektet

### Fil-för-fil:
```bash
# Exempel: Du har ändrat export_to_airtable_csv.py
copy C:\Users\robin\PycharmProjects\linkdb_dev_20250205\export_to_airtable_csv.py C:\Users\robin\PycharmProjects\linkdb\
```

## Tips & Tricks

### Skapa flera kopior
Du kan ha flera kopior samtidigt:
```
linkdb/                    ← Original (säker)
linkdb_dev_20250205/       ← Utveckling av export-funktioner
linkdb_experiment_api/     ← Experimentera med API
linkdb_refactor/           ← Stor refaktorering
```

### Namngivning
Använd beskrivande namn:
- `linkdb_dev_DATUM` - Generell utveckling
- `linkdb_feature_X` - Specifik feature
- `linkdb_test_Y` - Testa något specifikt
- `linkdb_backup_DATUM` - Backup innan stora ändringar

### Spara diskutrymme
Gamla kopior kan ta plats:
```bash
# Ta bort gamla kopior när du är klar
rmdir /s linkdb_dev_20250101
```

### Databaser
Kopian innehåller fullständiga kopior av alla databaser. Detta betyder:
- ✅ Du kan testa queries utan risk
- ✅ Du kan ändra schema
- ✅ Du kan ta bort/lägga till data
- ✅ Originalet påverkas inte

## Felsökning

### Problem: "Python not found"
**Lösning:** Kontrollera att Python är installerat och finns i PATH

### Problem: "Permission denied"
**Lösning:** Stäng alla program som har filer öppna från projektet

### Problem: Setup-scriptet misslyckas
**Lösning:** 
```bash
# Manuell setup
cd linkdb_dev_YYYYMMDD
python -m venv .venv
.venv\Scripts\activate
pip install rich openpyxl tldextract
```

### Problem: Import errors efter kopiering
**Lösning:** Kontrollera att du har aktiverat den nya virtuella miljön
```bash
.venv\Scripts\activate
```

## Exempel på output

```
═══════════════════════════════════════════════
  LinkDB Project Copy Tool
═══════════════════════════════════════════════

Nuvarande projekt: C:\Users\robin\PycharmProjects\linkdb

Projektinfo:
  • Filer att kopiera: 2,847
  • Total storlek: 156.3 MB
  • Exkluderade: __pycache__, *.pyc, *.pyo, .venv, venv...

Var vill du skapa kopian?
Standard: C:\Users\robin\PycharmProjects\<projektnamn>

Projektnamn [linkdb_dev_20250205]: 

✓ Skapar projektkopia: C:\Users\robin\PycharmProjects\linkdb_dev_20250205

Fortsätt med kopiering? [Y/n]: y

⠋ Kopierar filer... ████████████████████ 100%

Skapar utvecklingsfiler...

═══════════════════════════════════════════════
  Kopiering Klar!
═══════════════════════════════════════════════

Kopian skapad i: C:\Users\robin\PycharmProjects\linkdb_dev_20250205

Statistik:
  • Kopierade filer: 2,847
  • Total storlek: 156.3 MB
  • Överhoppade: 5 typer

Extra filer skapade:
  • README_COPY.md - Info om kopian
  • setup_dev_environment.bat - Setup-script för utveckling

Nästa steg:
  1. cd C:\Users\robin\PycharmProjects\linkdb_dev_20250205
  2. setup_dev_environment.bat (skapa .venv och installera dependencies)
  3. .venv\Scripts\activate (aktivera miljön)
  4. python show_columns.py (testa att allt fungerar)

Nu kan du utveckla fritt utan att påverka originalet!
```

## Checklista

- [ ] Kör `create_project_copy.py` eller `create_copy.bat`
- [ ] Kopian skapades framgångsrikt
- [ ] Gå till den nya mappen
- [ ] Kör `setup_dev_environment.bat`
- [ ] Aktivera `.venv\Scripts\activate`
- [ ] Testa med `python show_columns.py`
- [ ] Börja utveckla! 🚀

---

**OBS:** Originalprojektet i `C:\Users\robin\PycharmProjects\linkdb` förblir helt oförändrat och säkert!
# Guide: Skapa en säker projektkopia

## Varför skapa en kopia?

När du vill experimentera med nya funktioner eller göra stora ändringar är det smartast att arbeta i en kopia. På så sätt:
- ✅ Riskerar du inte att förstöra det fungerande originalet
- ✅ Kan du testa fritt utan oro
- ✅ Kan du alltid gå tillbaka till originalet om något går fel
- ✅ Har du en säker utvecklingsmiljö

## Snabbstart

### Alternativ 1: Dubbelklicka (enklast)
Dubbelklicka på:
```
create_copy.bat
```

### Alternativ 2: Kommandorad
```bash
python create_project_copy.py
```

## Vad händer?

Skriptet kommer att:

1. **Analysera projektet**
   - Räkna antal filer och total storlek
   - Visa vad som kommer att kopieras

2. **Fråga om destination**
   - Föreslår automatiskt namn: `linkdb_dev_YYYYMMDD`
   - Du kan ändra namnet om du vill
   - Kopian skapas i samma överordnade mapp som originalet

3. **Kopiera allt viktigt**
   - ✅ All Python-kod
   - ✅ Alla databaser (.db filer)
   - ✅ Excel-filer och data
   - ✅ Dokumentation
   - ✅ Scripts och batch-filer
   
4. **Exkludera onödigt**
   - ❌ `.venv` / `venv` (virtuella miljöer)
   - ❌ `__pycache__` (Python cache)
   - ❌ `.git` (versionshistorik)
   - ❌ `.idea` / `.vscode` (IDE-inställningar)
   - ❌ Temporära databasfiler

5. **Skapa setup-filer**
   - `README_COPY.md` - Förklaring av kopian
   - `setup_dev_environment.bat` - Automatisk setup

## Efter kopieringen

### Steg 1: Gå till den nya mappen
```bash
cd C:\Users\robin\PycharmProjects\linkdb_dev_YYYYMMDD
```

### Steg 2: Kör setup-scriptet
Dubbelklicka på `setup_dev_environment.bat` eller kör:
```bash
setup_dev_environment.bat
```

Detta kommer att:
- Skapa en ny virtuell miljö (`.venv`)
- Installera alla nödvändiga paket (rich, openpyxl, tldextract)
- Förbereda allt för utveckling

### Steg 3: Aktivera miljön (vid behov)
Vid framtida sessions:
```bash
.venv\Scripts\activate
```

### Steg 4: Testa att allt fungerar
```bash
python show_columns.py
```

Om detta fungerar är allt klart! 🎉

## Mappstruktur efter kopiering

```
linkdb_dev_YYYYMMDD/
├── README_COPY.md                    ← Info om kopian
├── setup_dev_environment.bat         ← Automatisk setup
├── .venv/                            ← Din nya virtuella miljö (skapas av setup)
├── app/
│   ├── build_all_customer_dbs.py
│   ├── build_history_db.py
│   ├── history_repo.py
│   └── ...
├── data/
│   ├── input/
│   │   └── main_sheet.xlsx
│   └── output/
│       ├── linkops_history.db
│       └── customers/
│           └── ...
├── build_customer_db.py

