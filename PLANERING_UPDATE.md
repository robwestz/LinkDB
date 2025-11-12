# ✅ PLANERING UPPDATERAD - Nya funktioner tillagda!

## 🎉 Vad som har lagts till:

### 1. **Publiceringssajt (OBLIGATORISK)** ✅
- Nytt fält: "Publiceringssajt"
- **Måste** anges när man lägger till länkar
- Validering: kan inte lägga till utan publiceringssajt

### 2. **Manuell målsida (VALFRI)** ✅
- Nytt fält: "Målsida"
- Kan anges om kunden har bestämd målsida
- Om tom: systemet väljer automatiskt från historik

### 3. **Manuell ankartext (VALFRI)** ✅
- Nytt fält: "Ankartext"
- Kan anges om kunden har bestämd ankartext
- Om tom: systemet genererar automatiskt

### 4. **Google Sheets Import** ✅
- Importera rader direkt från Google Sheets
- Kolumner: Domain, Kund, Targeting URL, Anchor
- Kräver credentials.json (se GOOGLE_SHEETS_SETUP.md)
- Alternativ: Manuell inmatning fungerar alltid!

---

## 📋 Nya fält i GUI:n:

### **Planering-fliken har nu:**

```
┌─────────────────────────────────────────────────┐
│ 1. Importera från Google Sheets ELLER lägg     │
│    till manuellt                                │
├─────────────────────────────────────────────────┤
│                                                 │
│ Google Sheets Import:                           │
│ [Google Sheets URL ................................]│
│ [Sheet namn (t.ex. November)]  [📥 Importera]  │
│                                                 │
│              ELLER                              │
│                                                 │
│ Lägg till manuellt:                             │
│ [Välj kund ▼]  [Antal länkar]                 │
│ [Publiceringssajt *]  [Målsida]               │
│ [Ankartext]  [Lägg till]                      │
│                                                 │
│ Tillagda länkar:                                │
│ • bethard.com                                   │
│   15 länkar på kingsizemag.se                   │
│   🎯 Målsida: https://bethard.com/sv/sports    │
│   📝 Ankar: "betting på fotboll"               │
│   [Ta bort]                                     │
└─────────────────────────────────────────────────┘
```

---

## 🔄 Hur det fungerar:

### **Alternativ 1: Google Sheets (med setup)**

1. Följ instruktioner i `GOOGLE_SHEETS_SETUP.md`
2. Lägg till `credentials.json` i projektmappen
3. Dela sheetet med service account email
4. I GUI: Ange Sheet URL och namn
5. Klicka **"📥 Importera"**
6. Alla rader läses in automatiskt! 🚀

### **Alternativ 2: Manuell inmatning (fungerar alltid!)**

1. Välj kund från dropdown
2. Ange antal länkar
3. **Ange publiceringssajt (MÅSTE fyllas i)**
4. Valfritt: Ange målsida
5. Valfritt: Ange ankartext
6. Klicka **"Lägg till"**
7. Upprepa för fler kunder
8. Klicka **"Generera plan"**

---

## 📊 Exempel på användning:

### **Manuell metod:**

```
Kund: bethard.com
Antal länkar: 15
Publiceringssajt: kingsizemag.se
Målsida: https://bethard.com/sv/sports
Ankartext: betting på fotboll

→ Klicka "Lägg till"
→ Visas i listan med alla detaljer
```

### **Google Sheets metod:**

```
Sheet innehåll:
Domain            | Kund         | Targeting URL                | Anchor
kingsizemag.se    | bethard.com  | bethard.com/sv/sports       | betting på fotboll
djungeltrumman.se | bethard.com  | bethard.com/sv/casino       | casino bonus
example.com       | cherry.com   |                              |

→ Klicka "Importera"
→ 3 rader importeras automatiskt
→ Visas i listan
```

---

## ✅ Validering:

### **Obligatoriska fält:**
- ✅ Kund (måste väljas)
- ✅ Antal länkar (måste vara > 0)
- ✅ **Publiceringssajt (NYTT - måste fyllas i)**

### **Valfria fält:**
- Målsida (om tom: använder historik)
- Ankartext (om tom: genereras automatiskt)

---

## 🎨 Uppdaterade filer:

### **Frontend:**
1. **templates/index.html** - Nya input-fält
2. **static/js/app.js** - Uppdaterad logik:
   - `addToPlan()` - Hanterar nya fält
   - `renderPlanItems()` - Visar pub_domain, målsida, ankar
   - `importFromSheets()` - Ny funktion för import
   - `detectVolume()` - Uppdaterad för ny datastruktur
   - `generatePlan()` - Uppdaterad för ny datastruktur

3. **static/css/style.css** - Styling för nya sektioner

### **Backend:**
4. **gui_app.py** - Nya endpoints:
   - `/api/import-sheets` - Importera från Google Sheets
   - Uppdaterad `/api/generate-plan` - Hanterar nya data

5. **Dokumentation:**
   - `GOOGLE_SHEETS_SETUP.md` - Steg-för-steg guide

---

## 🧪 Testa nu:

### **Steg 1: Ladda om sidan**
```
Ctrl + F5 (hard refresh)
```

### **Steg 2: Gå till Planering-fliken**
Du ska nu se:
- ✅ Google Sheets import-sektion (överst)
- ✅ "ELLER" separator
- ✅ Manuell input med nya fält

### **Steg 3: Testa manuell inmatning**
1. Välj "bethard.com"
2. Skriv "15" länkar
3. Skriv "kingsizemag.se" i Publiceringssajt
4. (Valfritt) Lägg till målsida och ankar
5. Klicka "Lägg till"

### **Steg 4: Kontrollera resultat**
- Kunden ska visas med alla detaljer
- Publiceringssajt ska synas
- Målsida och ankar (om angivna)

---

## 💡 Tips:

### **För Google Sheets:**
- Se `GOOGLE_SHEETS_SETUP.md` för setup
- Kolumnerna måste heta: **Domain**, **Kund**, **Targeting URL**, **Anchor**
- Kundnamn måste matcha i databasen

### **För Manuell input:**
- Du kan lägga till samma kund flera gånger med olika publiceringssajter
- Varje post kan ha olika målsida och ankartext
- Publiceringssajt-fältet lyser blått (obligatorisk)

### **Generera plan:**
- Systemet aggregerar alla länkar per kund
- Använder angivna målsidor och ankartexter när möjligt
- Genererar resten automatiskt

---

## 🐛 Om något inte fungerar:

### **Publiceringssajt kan inte lämnas tom:**
- Detta är med flit - publiceringssajt är **obligatorisk**
- Fältet får inte vara tomt
- Alert visas om du försöker

### **Google Sheets fungerar inte:**
- Normal! Kräver credentials.json setup
- Använd manuell metod istället
- Se `GOOGLE_SHEETS_SETUP.md` för att aktivera

### **Kan inte hitta kund:**
- Kunden måste finnas i databasen
- Kontrollera stavning
- Använd dropdown istället för att skriva

---

## ✅ Sammanfattning:

**Nytt:**
1. ✅ Publiceringssajt-fält (obligatorisk)
2. ✅ Målsida-fält (valfri)
3. ✅ Ankartext-fält (valfri)
4. ✅ Google Sheets import-funktion
5. ✅ Bättre visning av planerade länkar

**Fungerar:**
- ✅ Manuell inmatning
- ✅ Validering av obligatoriska fält
- ✅ Visning av alla detaljer
- ✅ Plangenerering med nya data

**Nästa:**
- Google Sheets credentials setup (frivilligt)
- Testa med verklig data
- Generera första riktiga planen!

---

**🎊 Planering-fliken är nu mycket kraftfullare!**

**TESTA:** Ladda om och prova att lägga till länkar manuellt! 🚀

---

## 📖 Relaterade filer:

- `GOOGLE_SHEETS_SETUP.md` - Setup för Google Sheets
- `GUI_README.md` - Allmän GUI-dokumentation
- `PLANNING_SYSTEM_SPEC.md` - Systemspecifikation

