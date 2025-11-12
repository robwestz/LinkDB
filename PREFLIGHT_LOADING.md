# ✅ PREFLIGHT-LADDNING & CLIENT INDEX IMPLEMENTERAD!

## 🎉 Vad som har implementerats:

### **1. Client Index med customer_id-matchning** ✅

**Fil:** `data/client_index_matched.xlsx`

**Kolumner:**
- `customer_id` - Matchad från databas (69 av 119 matchade)
- `customer_name` - Kundnamn
- `marknad` - Marknad (SE/NO/FI etc)
- `client_domain` - Kundens rotdomän
- `monthly_budget` - Månatlig budget
- `other_info` - Övrig info

**Script:** `data/match_customer_ids.py`
- Matchar automatiskt customer_id från databas
- 3 matchningsmetoder (exakt, LIKE, brand)
- Rapporterar ej funna kunder

### **2. Preflight-laddning från Google Sheets** ✅

**Ny workflow:**

```
Steg 1: Ladda preflight
  → Läser pub_domain + kund från Google Sheets (rad 2-175)
  → Matchar mot client_index
  → Validerar kund-domäner
  ↓
Steg 2: Granska & Redigera
  → Lägg till målsidor/ankartexter
  → Redigera pub_domains
  ↓
Steg 3: Analysera kunders planering
  → Semantisk preflight
  → Target URL-validering (matchar client_domain)
  ↓
Steg 4: Generera plan
  → AI-prompt
  → Färdig plan
```

### **3. Target URL-validering** ✅

**Validerar att:**
- Varje target_url börjar med kundens client_domain
- Exempel: bethard.com måste ha URLs som börjar med "bethard.com"
- Fel flaggas innan plangenerering

**Validator:** `app/validators/target_url_validator.py`

---

## 🔧 Nya endpoints:

### **POST /api/load-preflight**

Laddar preflight från Google Sheets och validerar mot client_index.

**Request:**
```json
{
  "sheets_url": "https://docs.google.com/spreadsheets/d/...",
  "sheet_name": "November",
  "start_row": 2,
  "end_row": 175
}
```

**Response:**
```json
{
  "preflight_items": [
    {
      "row": 2,
      "pub_domain": "kingsizemag.se",
      "customer_id": 117,
      "customer_name": "Bethard",
      "client_domain": "bethard.com"
    }
  ],
  "total_items": 150,
  "total_customers": 25,
  "customer_summary": [...],
  "validation_errors": [...],
  "skipped": [...]
}
```

### **POST /api/semantic-preflight** (uppdaterad)

Nu inkluderar target URL-validering.

**Tillagt i response:**
```json
{
  "url_validation": {
    "valid": false,
    "errors": [
      "Target URL 'https://wrong.com' matchar inte domän 'bethard.com'"
    ],
    "warnings": [...],
    "total_errors": 3,
    "total_warnings": 1
  }
}
```

---

## 📊 GUI-ändringar:

### **Planering-fliken - Ny design:**

```
┌──────────────────────────────────────────────────────────┐
│ 1. Skapa månadens planering automatiskt                  │
├──────────────────────────────────────────────────────────┤
│                                                           │
│ Ladda in oplanerad preflight från Google Sheets          │
│ (pub_domain + kund per rad)                              │
│                                                           │
│ [Google Sheets URL.............................] [Flik] │
│ [Startrad: 2] [Slutrad: 175] [📥 Ladda preflight (steg 1)]│
│                                                           │
│ Läser kolumnerna: Domain (pub_domain) och Kund          │
└──────────────────────────────────────────────────────────┘

ELLER

[Import från Google Sheets...]
[Manuell inmatning...]
```

---

## 🎯 Workflow-exempel:

### **Scenario: November 2025-planering**

**1. Ladda preflight:**
```
Google Sheets: November-fliken
Rader: 2-175
Klicka: "📥 Ladda preflight"

Resultat:
✅ Preflight laddad från November!
25 kunder
150 länkar totalt
⚠️ Valideringsfel: 3
  • Rad 15: Kund 'Unknown AB' saknas i client_index
  ... och 2 till
```

**2. Granska:**
```
Listan visar:
• bethard.com
  10 länkar på kingsizemag.se
  [Ta bort]

• cherry.com
  8 länkar på djungeltrumman.se
  [Ta bort]
```

**3. Lägg till målsidor (valfritt):**
```
Redigera länkar manuellt:
- Klicka på en länk
- Lägg till målsida
- Lägg till ankartext
```

**4. Analysera:**
```
Klicka: "2️⃣ Analysera kunders planering"

Resultat visar:
✅ Semantisk analys klar
✅ URL-validering: Alla OK
ELLER
❌ URL-valideringsfel (3):
  • Target URL 'https://wrong.com/page' matchar inte domän 'bethard.com'
  
⚠️ Fixa dessa fel innan du fortsätter!
```

**5. Generera:**
```
Om valid:
  Klicka: "3️⃣ Generera plan"
  → AI-prompt
  → Färdig plan
  → CSV
```

---

## 🔍 Client Index-matchning:

### **Kördes:**
```bash
python data/match_customer_ids.py
```

### **Resultat:**
```
Matchade: 69
Ej funna: 50

✓ bethard.com → customer_id: 117
✓ cherry.com → customer_id: 110
✓ hajper.com → customer_id: 134
✗ Leovegas → NOT FOUND
✗ Vera&John → NOT FOUND
```

### **Ej funna kunder:**

Dessa 50 kunder finns i client_index men inte i databasen:
- Aerius Ventilation
- Cdbilvrd
- A Retro Tale
- ... (och 47 till)

**Åtgärd:** Lägg till dem i databasen eller ta bort från client_index.

---

## 🛡️ Target URL-validering:

### **Regler:**

1. **Varje target_url måste börja med kundens client_domain**

Exempel:
```
✅ Valid:
customer_id: 117 (bethard.com)
target_url: https://bethard.com/sv/sports
client_domain: bethard.com
→ "bethard.com/sv/sports" börjar med "bethard.com" ✅

❌ Invalid:
customer_id: 117 (bethard.com)
target_url: https://cherry.com/page
client_domain: bethard.com
→ "cherry.com/page" börjar INTE med "bethard.com" ❌
```

2. **Normalisering innan validering:**
```python
# Tar bort:
- http://
- https://
- www.

# Så att alla dessa är valid:
https://www.bethard.com/page
http://bethard.com/page
www.bethard.com/page
bethard.com/page
```

3. **Fel blockerar plangenerering:**

Om URL-valideringsfel finns:
- Analys-dialog visar felen
- "Fortsätt"-knappen är synlig MEN
- Användaren varnas att fixa felen först
- Best practice: Fixa innan fortsättning

---

## 📁 Nya/uppdaterade filer:

### **Nya:**
1. `data/match_customer_ids.py` - Matchningscript
2. `data/client_index_matched.xlsx` - Matchad client index
3. `app/validators/target_url_validator.py` - URL-validator

### **Uppdaterade:**
1. `gui_app.py`:
   - `/api/load-preflight` endpoint
   - URL-validering i `/api/semantic-preflight`
   - Pandas import för Excel-läsning

2. `templates/index.html`:
   - Ny preflight-sektion
   - Startrad/slutrad inputs
   - Uppdaterad hjälptext

3. `static/js/app.js`:
   - `loadPreflight()` funktion
   - URL-validering i analys-dialog
   - `preflight_loaded` workflow status

---

## 🧪 Testning:

### **1. Testa client_index-matchning:**
```bash
python data/match_customer_ids.py
```

### **2. Testa URL-validator:**
```bash
python app/validators/target_url_validator.py
```

### **3. Testa preflight-laddning:**
```
1. Öppna GUI: http://127.0.0.1:5000
2. Gå till Planering
3. Se lila sektionen överst
4. Kontrollera att:
   - Google Sheets URL är ifylld
   - Flik: November
   - Startrad: 2
   - Slutrad: 175
5. Klicka "📥 Ladda preflight"
6. Se resultat
```

---

## ⚠️ Observera:

### **Google Sheets credentials krävs:**

För att ladda från Google Sheets behövs `credentials.json`.

**Om den saknas:**
- Användaren får felmeddelande
- Kan använda manuell inmatning istället
- Se `GOOGLE_SHEETS_SETUP.md` för instruktioner

### **Client index måste vara matchad:**

Innan preflight kan laddas måste:
```bash
python data/match_customer_ids.py
```
köras för att skapa `client_index_matched.xlsx`.

### **Target URL-validering är strikt:**

Om en målsida inte matchar kundens domän:
- Fel flaggas i analys
- Plangenerering bör inte fortsätta
- Fixa URL:en eller ta bort länken

---

## 💡 Best Practices:

### **1. Förbered client_index:**
```bash
1. Uppdatera data/client_index.xlsx med alla kunder
2. Kör: python data/match_customer_ids.py
3. Granska: data/client_index_matched.xlsx
4. Lägg till ej funna kunder i databasen
```

### **2. Ladda preflight:**
```
1. Öppna Google Sheets
2. Kontrollera att kolumnerna heter: Domain, Kund
3. Verifiera att alla kunder finns i client_index
4. Ladda in i GUI
```

### **3. Validera innan planering:**
```
1. Granska laddade länkar
2. Lägg till målsidor för viktiga länkar
3. Kör "Analysera kunders planering"
4. Fixa alla URL-valideringsfel
5. Fortsätt till plangenerering
```

---

## 🎊 Sammanfattning:

**NYA FEATURES:**
1. ✅ Client Index med customer_id-matchning
2. ✅ Preflight-laddning från Google Sheets
3. ✅ Target URL-validering mot client_domain
4. ✅ Valbart rad-intervall (2-175)
5. ✅ Validering i semantisk preflight

**WORKFLOW:**
```
Ladda preflight → Granska → Analysera (validerar URLs) → Generera
```

**SÄKERHET:**
- Target URLs valideras mot client_domain
- Fel blockerar plangenerering
- Transparent valideringsrapportering

**Detta säkerställer att ingen länk pekar till fel domän! 🛡️**

---

## 📖 Relaterade filer:

- `GOOGLE_SHEETS_SETUP.md` - Setup för credentials
- `AUTOMATIC_MONTHLY_GENERATION.md` - Automatisk generering
- `SELF_CORRECTION.md` - Självkorrigering
- `AI_PLANNING_GUIDE.md` - AI-assisterad planering

---

**🚀 Ladda om GUI och testa preflight-laddning! Rad 2-175 från November-fliken!**

