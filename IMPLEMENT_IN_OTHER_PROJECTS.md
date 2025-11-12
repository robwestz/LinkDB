# Guide: Använda kopieringssystemet i ANDRA projekt

## 🎯 Snabb implementering (3 sätt)

### Metod 1: Kopiera en fil (enklast!)

**Kopiera bara denna fil till ditt nya projekt:**
```
copy_any_project.py
```

**Kör den i det nya projektet:**
```bash
cd C:\MittAndraProject
python copy_any_project.py
```

**Klart!** ✅

---

### Metod 2: Kopiera komplett system (alla features)

**Kopiera dessa filer till ditt nya projekt:**
```
create_project_copy.py
create_copy.bat
```

**Kopiera också dokumentation (valfritt):**
```
GUIDE_PROJECT_COPY.md
COPY_QUICKSTART.md
```

---

### Metod 3: Anpassa för specifikt projekt

1. Kopiera `copy_any_project.py` till ditt projekt
2. Öppna filen och anpassa `EXCLUDE_PATTERNS` för ditt projekt
3. Kör den!

---

## 📋 Steg-för-steg: Implementera i befintligt projekt

### Exempel: Lägga till i ett Flask-projekt

```bash
# 1. Gå till ditt Flask-projekt
cd C:\MyFlaskApp

# 2. Kopiera verktyget (från linkdb-projektet)
copy C:\Users\robin\PycharmProjects\linkdb\copy_any_project.py .

# 3. Kör det!
python copy_any_project.py

# 4. Följ instruktionerna
# Projektet identifieras automatiskt
# Kopia skapas med alla filer
```

### Exempel: Lägga till i ett Django-projekt

```bash
cd C:\MyDjangoProject
copy C:\Users\robin\PycharmProjects\linkdb\copy_any_project.py .
python copy_any_project.py
```

### Exempel: Lägga till i ett Data Science-projekt

```bash
cd C:\MyDataProject
copy C:\Users\robin\PycharmProjects\linkdb\copy_any_project.py .
python copy_any_project.py
```

---

## 🔧 Anpassa för olika projekttyper

### Python-projekt med requirements.txt

**Inget behöver ändras!** Verktyget upptäcker automatiskt `requirements.txt` och installerar dependencies.

### Python-projekt med poetry/pipenv

Öppna `copy_any_project.py` och ändra i `create_setup_script()`:

```python
# För Poetry
requirements_cmd = "poetry install"

# För Pipenv
requirements_cmd = "pipenv install"
```

### Django-projekt

Lägg till Django-specifika exkluderingar:

```python
EXCLUDE_PATTERNS = [
    # ...existing patterns...
    '*.sqlite3',
    'db.sqlite3',
    'media/',
    'staticfiles/',
    '*.pyc',
]
```

### Flask-projekt

Lägg till Flask-specifika exkluderingar:

```python
EXCLUDE_PATTERNS = [
    # ...existing patterns...
    'instance/',
    '*.db',
    'uploads/',
]
```

### Data Science / Jupyter-projekt

Lägg till data-specifika exkluderingar:

```python
EXCLUDE_PATTERNS = [
    # ...existing patterns...
    '*.csv',  # Om stora CSV-filer
    '*.parquet',
    '*.h5',
    'data/raw/',  # Om stora rådata
    '.ipynb_checkpoints',
    '*.pkl',
]
```

---

## 📁 Var placerar man filen?

### Alternativ 1: I projektroten (rekommenderat)
```
MyProject/
├── copy_any_project.py  ← Lägg här
├── src/
├── tests/
├── requirements.txt
└── README.md
```

### Alternativ 2: I en tools/scripts-mapp
```
MyProject/
├── tools/
│   └── copy_any_project.py  ← Eller här
├── src/
└── ...
```

Kör sedan: `python tools/copy_any_project.py`

---

## 🎨 Exempel på anpassningar

### Lägg till fler exkluderingsmönster

```python
EXCLUDE_PATTERNS = [
    # Originalet
    '__pycache__',
    '.venv',
    '.git',
    
    # Dina tillägg för specifikt projekt
    'temp/',
    'backup/',
    '*.bak',
    'old/',
    'archive/',
]
```

### Ändra destination-mapp

```python
# Standard: Skapar kopia i samma överordnade mapp
parent_dir = CURRENT_PROJECT.parent

# Alternativ: Skapar alltid kopior i en specifik mapp
parent_dir = Path("C:/Dev/Copies")
```

### Anpassa auto-genererad README

Redigera `create_readme_for_copy()` funktionen för att lägga till projektspecifika instruktioner.

---

## 💡 Användningsexempel

### Scenario 1: Nytt Flask-projekt

```bash
# Skapa Flask-projekt
cd C:\FlaskBlog
# ... utveckla projektet ...

# Vill testa ny feature - skapa kopia
python copy_any_project.py
# Namn: FlaskBlog_test_auth

cd ..\FlaskBlog_test_auth
setup_dev_environment.bat
.venv\Scripts\activate

# Utveckla auth-feature
# Testa
# Om det fungerar → kopiera tillbaka till original
```

### Scenario 2: Django e-commerce

```bash
cd C:\DjangoShop
python copy_any_project.py
# Namn: DjangoShop_payment_refactor

# Refaktorera payment-modulen i kopian
# Testa grundligt
# Kopiera tillbaka när det fungerar
```

### Scenario 3: Machine Learning-projekt

```bash
cd C:\ML_Project
python copy_any_project.py
# Namn: ML_Project_experiment_xgboost

# Experimentera med nya modeller
# Alla data och notebooks kopierade
# Original påverkas inte
```

---

## 🚀 Quick Reference Commands

### Implementera i nytt projekt
```bash
# Gå till projektet
cd C:\MittProjekt

# Kopiera verktyget
copy C:\Users\robin\PycharmProjects\linkdb\copy_any_project.py .

# Kör
python copy_any_project.py
```

### Anpassa exkluderingar
```python
# Öppna copy_any_project.py
# Hitta EXCLUDE_PATTERNS
# Lägg till dina mönster
EXCLUDE_PATTERNS = [
    # ... standard ...
    'din_mapp/',
    '*.din_ext',
]
```

### Skapa kopia
```bash
python copy_any_project.py
# Följ instruktionerna
```

---

## 📚 Filöversikt för olika implementeringar

### Minimal (1 fil)
```
copy_any_project.py  ← Detta räcker!
```

### Standard (2 filer)
```
copy_any_project.py
create_copy.bat      ← För Windows dubbelklick
```

### Komplett (4+ filer)
```
copy_any_project.py
create_copy.bat
GUIDE_PROJECT_COPY.md
COPY_QUICKSTART.md
QUICK_COPY_GUIDE.txt
```

---

## ⚙️ Tekniska detaljer

### Vad verktyget gör automatiskt:

1. **Identifierar projekt:**
   - Läser `pyproject.toml`
   - Läser `setup.py`
   - Fallback: använder mappnamn

2. **Analyserar storlek:**
   - Räknar filer
   - Beräknar total storlek
   - Visar innan kopiering

3. **Kopierar smart:**
   - Exkluderar onödiga filer
   - Behåller mappstruktur
   - Kopierar filattribut (timestamps etc.)

4. **Skapar setup:**
   - `README_COPY.md` - Info om kopian
   - `setup_dev_environment.bat` - Auto-setup
   - Upptäcker `requirements.txt` automatiskt

---

## 🔍 Felsökning

### Problem: "ModuleNotFoundError: No module named 'rich'"

**Lösning:**
```bash
pip install rich
```

### Problem: Fel projekt kopieras

**Lösning:** Kontrollera att du är i rätt mapp när du kör scriptet:
```bash
cd C:\RättProjekt
python copy_any_project.py
```

### Problem: Vissa filer ska inte exkluderas

**Lösning:** Ta bort från `EXCLUDE_PATTERNS` i scriptet

### Problem: Vissa filer ska exkluderas men kopieras ändå

**Lösning:** Lägg till i `EXCLUDE_PATTERNS`

---

## ✅ Checklista: Implementera i nytt projekt

- [ ] Kopiera `copy_any_project.py` till projektet
- [ ] (Valfritt) Kopiera `create_copy.bat` för enkel användning
- [ ] (Valfritt) Anpassa `EXCLUDE_PATTERNS` för projektet
- [ ] Testa: `python copy_any_project.py`
- [ ] Verifiera att kopian fungerar
- [ ] Börja utveckla i kopian!

---

## 🎯 Sammanfattning

### För att använda i ett NYTT projekt:

**1 fil behövs:** `copy_any_project.py`

**3 kommandon:**
```bash
cd C:\MittNyaProjekt
copy C:\...\linkdb\copy_any_project.py .
python copy_any_project.py
```

**Klart!** Nu kan du skapa säkra kopior av vilket Python-projekt som helst! 🎉

---

## 📖 Mer information

- Se `GUIDE_PROJECT_COPY.md` för detaljerad guide om kopieringssystemet
- Se `COPY_QUICKSTART.md` för snabbreferens
- Se `README_OVERVIEW.md` för översikt av LinkDB-projektet

---

**Tips:** Lägg till `copy_any_project.py` i dina projektmallar så har du alltid verktyget tillgängligt! 💡

