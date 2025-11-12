# 🚀 Kom igång UTAN Google Sheets API

## ✅ Enklaste lösningen: Manuell inmatning

Du behöver INTE Google Sheets API för att använda systemet! Här är alternativa sätt:

---

## Metod 1: Manuell inmatning (REKOMMENDERAT)

### Snabbt och enkelt:

1. Öppna ditt Google Sheet
2. För varje rad:
   - Kopiera **Domain** → Klistra in "Publiceringssajt"
   - Välj **Kund** från dropdown
   - Kopiera **Targeting URL** → Klistra in "Målsida" (om finns)
   - Kopiera **Anchor** → Klistra in "Ankartext" (om finns)
   - Klicka "Lägg till"
3. Upprepa för alla rader
4. Klicka "Generera plan"

**Tid:** ~2-3 minuter för 20 länkar

---

## Metod 2: CSV Export + Manuell batch

### Om du har många länkar:

1. Exportera ditt Google Sheet som CSV
2. Öppna CSV i Excel/Notepad
3. Kopiera data rad för rad
4. Klistra in i GUI:n

**Fördel:** Snabbare för 50+ länkar

---

## Metod 3: Python-script (för power users)

### Skapa ett script som läser CSV:

```python
import csv
import requests

# Läs CSV från Google Sheets export
with open('november_links.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        data = {
            'customer_name': row['Kund'],
            'pub_domain': row['Domain'],
            'target_url': row.get('Targeting URL', ''),
            'anchor_text': row.get('Anchor', '')
        }
        
        # Lägg till via GUI eller direkt i databas
        print(f"Lägg till: {data}")
```

---

## Metod 4: Google Sheets API (Avancerat)

### Om du verkligen vill ha automatisk import:

Se **GOOGLE_SHEETS_SETUP.md** för fullständig guide.

**Kräver:**
1. Google Cloud Project
2. Service Account
3. credentials.json-fil
4. Dela sheet med service account

**Tid för setup:** ~15 minuter första gången

---

## 💡 Rekommendation:

### För 1-20 länkar per månad:
→ **Manuell inmatning** (snabbast totalt sett)

### För 20-50 länkar:
→ **CSV Export + batch** (bra balans)

### För 50+ länkar eller automatisering:
→ **Google Sheets API** (värt setup-tiden)

---

## 🎯 Snabbguide: Manuell inmatning

### Exempel med bethard.com:

**I Google Sheet:**
```
Domain: kingsizemag.se
Kund: bethard.com
Targeting URL: https://bethard.com/sv/sports
Anchor: betting på fotboll
```

**I GUI (Planering-fliken):**

1. **Välj kund:** bethard.com (från dropdown)
2. **Antal länkar:** 1
3. **Publiceringssajt:** kingsizemag.se
4. **Målsida:** https://bethard.com/sv/sports
5. **Ankartext:** betting på fotboll
6. **Klicka:** "Lägg till"

**Upprepa för nästa rad!**

---

## ⚡ Pro tips:

### Tips 1: Använd tangentbord
- Tab för att hoppa mellan fält
- Enter för att "Lägg till"
- Ctrl+C / Ctrl+V för copy/paste

### Tips 2: Gruppera per kund
Lägg till alla länkar för en kund i taget:
- bethard.com (alla länkar)
- cherry.com (alla länkar)
- hajper.com (alla länkar)

### Tips 3: Målsida och ankar är valfria
Du kan hoppa över dem om:
- Systemet ska välja automatiskt från historik
- Du vill att AI ska generera ankartexter

### Tips 4: Granska innan generering
Se över alla tillagda länkar innan "Generera plan"

---

## 🐛 Felsökning:

### Problem: "Kund hittades inte"
**Lösning:** 
- Kunden måste finnas i databasen
- Kontrollera stavning i Google Sheet
- Använd exakt samma namn som i dropdown

### Problem: "Publiceringssajt krävs"
**Lösning:**
- Detta fält är obligatoriskt
- Kan inte lämnas tomt
- Ange domain utan http:// (t.ex. "example.com")

### Problem: "För långsamt att lägga till manuellt"
**Lösning:**
- Överväg Google Sheets API
- Eller skapa Python-script
- Eller exportera färre länkar per gång

---

## ✅ Sammanfattning:

**Google Sheets API är INTE obligatoriskt!**

**Fungerar utan setup:**
- ✅ Manuell inmatning
- ✅ CSV-baserad workflow
- ✅ Python-script
- ✅ Direkt databasmanipulation

**Google Sheets API behövs bara för:**
- 🔄 Automatisk import med en knapptryckning
- 📊 Stora volymer (50+ länkar)
- ⚙️ Integration i automatiserad pipeline

**Rekommendation:** Börja med manuell inmatning, uppgradera till API om du märker att du behöver det!

---

## 📖 Relaterade guides:

- **GOOGLE_SHEETS_SETUP.md** - Om du vill ha automatisk import
- **PLANERING_UPDATE.md** - Alla planeringsfeatures
- **AI_PLANNING_GUIDE.md** - AI-assisterad planering
- **GUI_README.md** - Allmän dokumentation

