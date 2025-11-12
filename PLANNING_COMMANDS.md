# KOMMANDON - Intelligent Link Planning System

## 🚀 Snabbkommandon

### Initiera systemet
```bash
cd C:\Users\robin\PycharmProjects\linkdb
python init_planning_system.py
```

### Testa Customer Grouper
```bash
python app/planning/customer_grouper.py
```

### Testa Link History Analyzer  
```bash
python app/analyzers/link_history_analyzer.py
```

### Testa Monthly Link Viewer (ny!)
```bash
python app/analyzers/monthly_link_viewer.py
```

### Testa Volume Detector (ny!)
```bash
python app/planning/volume_detector.py
```

### Initiera bara databasen
```bash
python app/planning/db_manager.py
```

eller med force (återskapa):
```bash
python app/planning/db_manager.py --force
```

---

## 📦 Installation

### Installera alla dependencies
```bash
pip install -r requirements_planning.txt
```

### Installera spaCy-modeller (för Fas 2)
```bash
# Svenska
python -m spacy download sv_core_news_sm

# Engelska
python -m spacy download en_core_web_sm
```

---

## 🐍 Python-exempel

### Analysera en specifik kund
```python
from app.analyzers.link_history_analyzer import LinkHistoryAnalyzer

analyzer = LinkHistoryAnalyzer("data/output/linkops_history.db")
analysis = analyzer.analyze_customer(117)  # bethard.com

if analysis:
    analyzer.print_analysis(analysis)
    
    # Få specifika värden
    print(f"Total links: {analysis.total_links}")
    print(f"Diversity: {analysis.anchor_diversity_score}")
    print(f"Strategy: {analysis.primary_strategy}")
```

### Gruppera kunder
```python
from app.planning.customer_grouper import CustomerGrouper

# Från planeringsdokument (simulerat)
customer_counts = {
    117: 15,
    118: 5,
    119: 25,
}

grouper = CustomerGrouper("data/output/linkops_history.db")
groups = grouper.group_customers(customer_counts)

# Visa sammanfattning
grouper.print_summary(groups)

# Loopa genom grupperna
for group in groups:
    print(f"{group.canonical_root}: {group.recommended_strategy}")
```

### Initiera planning database programmatiskt
```python
from app.planning.db_manager import PlanningDBManager

manager = PlanningDBManager("data/output/linkops_planning.db")
manager.initialize_database(force=False)
manager.add_default_strategies()
manager.print_status()
```

---

## 🗄️ Databas-kommandon

### Kolla databas status
```python
from app.planning.db_manager import PlanningDBManager

manager = PlanningDBManager("data/output/linkops_planning.db")
counts = manager.get_table_counts()

for table, count in counts.items():
    print(f"{table}: {count} rows")
```

### SQLite direkt
```bash
# Öppna planning database
sqlite3 data/output/linkops_planning.db

# Visa tabeller
.tables

# Visa strategier
SELECT * FROM planning_strategies;

# Räkna planer
SELECT COUNT(*) FROM link_plans;

# Avsluta
.quit
```

---

## 📊 Export-kommandon

### Exportera customer_id till CSV
```bash
python export_customer_by_id.py 117
```

### Lista alla kunder
```bash
python export_customer_by_id.py --list
```

### Exportera alla kunder till Airtable
```bash
python export_to_airtable_csv.py
```

### Avancerad export
```bash
python export_advanced.py --list
python export_advanced.py --customers "1-50"
python export_advanced.py --domain ".se"
```

---

## 🔍 Felsökning

### Kolla om databaser finns
```bash
dir data\output\*.db
```

### Testa imports
```python
# Testa att moduler kan importeras
from app.planning.customer_grouper import CustomerGrouper
from app.analyzers.link_history_analyzer import LinkHistoryAnalyzer
from app.planning.db_manager import PlanningDBManager

print("✅ All imports successful!")
```

### Kolla Python-version
```bash
python --version
# Behöver Python 3.8+
```

### Lista installerade paket
```bash
pip list | grep -E "(rich|spacy|gensim|sklearn)"
```

---

## 🔄 Utvecklingskommandon

### Skapa projektkopia för utveckling
```bash
python create_project_copy.py
# eller
python quick_copy.py
```

### Aktivera virtuell miljö
```bash
.venv\Scripts\activate
```

### Installera i development mode
```bash
pip install -e .
```

---

## 📚 Dokumentation

### Öppna dokumentation
```bash
# Windows
start PLANNING_SYSTEM_SPEC.md
start README_PLANNING.md
start PLANNING_QUICKSTART.md

# Eller öppna i editor
code PLANNING_SYSTEM_SPEC.md
```

### Generera dokumentation (framtida)
```bash
# När vi har docstrings
pydoc app.planning.customer_grouper
pydoc app.analyzers.link_history_analyzer
```

---

## 🧪 Test-kommandon (framtida)

### Kör unit tests
```bash
pytest tests/
```

### Kör specifikt test
```bash
pytest tests/test_customer_grouper.py
```

### Kör med coverage
```bash
pytest --cov=app tests/
```

---

## 🚢 Deployment (framtida)

### Bygg distribution
```bash
python setup.py sdist bdist_wheel
```

### Installera från wheel
```bash
pip install dist/linkdb_planning-1.0.0-py3-none-any.whl
```

---

## 💡 Tips & Tricks

### Kör Python one-liner
```bash
# Snabb analys
python -c "from app.analyzers.link_history_analyzer import LinkHistoryAnalyzer; a = LinkHistoryAnalyzer('data/output/linkops_history.db'); print(a.analyze_customer(117).total_links)"

# Snabb gruppering
python -c "from app.planning.customer_grouper import CustomerGrouper; g = CustomerGrouper('data/output/linkops_history.db'); print(g.classify_by_volume(15))"
```

### Alias (PowerShell)
```powershell
# Lägg till i PowerShell profile
Set-Alias -Name analyze -Value "python app/analyzers/link_history_analyzer.py"
Set-Alias -Name group -Value "python app/planning/customer_grouper.py"
Set-Alias -Name initplan -Value "python init_planning_system.py"
```

### Environment variables
```bash
# Sätt databas-path
$env:LINKDB_HISTORY = "C:\Users\robin\PycharmProjects\linkdb\data\output\linkops_history.db"
$env:LINKDB_PLANNING = "C:\Users\robin\PycharmProjects\linkdb\data\output\linkops_planning.db"
```

---

## 📖 Hjälpkommandon

### Visa hjälp för script
```bash
python export_customer_by_id.py --help
python export_advanced.py --help
```

### Visa module docstring
```python
import app.planning.customer_grouper
print(app.planning.customer_grouper.__doc__)
```

### Lista funktioner i modul
```python
import app.planning.customer_grouper
print(dir(app.planning.customer_grouper))
```

---

## 🎯 Workflow-exempel

### Komplett workflow
```bash
# 1. Initiera
python init_planning_system.py

# 2. Analysera historik
python app/analyzers/link_history_analyzer.py

# 3. Gruppera kunder (från planeringsdokument)
python app/planning/customer_grouper.py

# 4. Generera planer (kommer i Fas 1)
# python app/planning/plan_generator.py --sheet-url "..."

# 5. Exportera resultat
# python export_planning_results.py
```

---

## 🔗 Användbara länkar

- **Planning Spec:** `PLANNING_SYSTEM_SPEC.md`
- **README:** `README_PLANNING.md`
- **Quickstart:** `PLANNING_QUICKSTART.md`
- **Google Sheets:** https://docs.google.com/spreadsheets/d/1KfON8-Y7lCW9XtYnnY9uxdmlojyCl5QxQALtn8FH5YE/

---

**💡 Pro tip:** Lägg till dessa kommandon i ditt README eller skapa alias för de du använder ofta!

