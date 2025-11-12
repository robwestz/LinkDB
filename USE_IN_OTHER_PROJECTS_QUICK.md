# ⚡ SNABBGUIDE: Använd i VILKET projekt som helst!

## 🎯 3 Steg för att använda i ett annat projekt

### Steg 1: Kopiera filen
```bash
copy C:\Users\robin\PycharmProjects\linkdb\copy_any_project.py C:\MittAndraProject\
```

### Steg 2: Gå till projektet
```bash
cd C:\MittAndraProject
```

### Steg 3: Kör!
```bash
python copy_any_project.py
```

**✅ Klart! Nu kan du skapa säkra kopior av vilket projekt som helst!**

---

## 📋 Exempel: Flask-projekt

```bash
cd C:\MyFlaskApp
copy C:\...\linkdb\copy_any_project.py .
python copy_any_project.py
# → Följ instruktionerna
# → Kopian skapas med alla filer
```

## 📋 Exempel: Django-projekt

```bash
cd C:\MyDjangoSite
copy C:\...\linkdb\copy_any_project.py .
python copy_any_project.py
```

## 📋 Exempel: Data Science-projekt

```bash
cd C:\MyMLProject
copy C:\...\linkdb\copy_any_project.py .
python copy_any_project.py
```

---

## 🎨 Anpassa för ditt projekt

Öppna `copy_any_project.py` och ändra `EXCLUDE_PATTERNS`:

```python
EXCLUDE_PATTERNS = [
    # Standard (behåll dessa)
    '__pycache__',
    '.venv',
    '.git',
    
    # Lägg till för ditt projekt:
    'temp/',           # Temporära filer
    '*.bak',           # Backup-filer
    'large_data/',     # Stora datafiler
    'my_exclude/',     # Din mapp
]
```

---

## 🌟 Features

✅ Fungerar med **VILKET** Python-projekt som helst
✅ Identifierar projekt automatiskt
✅ Upptäcker `requirements.txt`
✅ Exkluderar .venv, cache, etc.
✅ Skapar setup-script automatiskt
✅ Progress bars och fin output

---

## 📚 Mer detaljer

Se **IMPLEMENT_IN_OTHER_PROJECTS.md** för:
- Anpassningar för olika projekttyper
- Django/Flask/Data Science exempel
- Detaljerade instruktioner
- Felsökning

---

## 💡 Tips

**Lägg i dina projektmallar:**
Kopiera `copy_any_project.py` till dina projektmallar så har du alltid tillgång till det!

**Dela med teamet:**
Denna fil fungerar fristående - dela med ditt team!

**Anpassa en gång:**
Anpassa `EXCLUDE_PATTERNS` för din typ av projekt, sedan funkar det överallt!

---

**🎉 Nu kan du skapa säkra kopior av ALLA dina projekt!**

