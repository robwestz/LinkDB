# ✅ MAIN SHEET VIEWER SKAPAD!

## 🎉 Vad som har implementerats:

### **1. Ny flik "Main Sheet" i GUI** ✅

En komplett viewer för `main_sheet.xlsx` med:
- 📊 **4829 rader** total data
- 🔍 **Sökfunktion** med filter
- 📋 **Tabell-vy** med alla kolumner
- 📈 **Statistik** (totalt, visas, unika kunder)
- ⚡ **Paginering** (100 rader åt gången)

---

## 🎯 Features:

### **Sökfunktion:**
- Sök i alla kolumner samtidigt
- Eller filtrera på specifik kolumn:
  - Canonical Root
  - Pub URL
  - Target URL
  - Anchor Text
  - Brand

### **Tabell-visning:**
```
# | Canonical Root | Brand | Pub URL | Target URL | Anchor Text | Type | Published
```

### **Statistik:**
- **Totalt:** 4829 länkar
- **Visas:** Antal rader i aktuell vy
- **Unika kunder:** Antal unika canonical_root

### **Paginering:**
- Laddar 100 rader åt gången
- "Ladda fler"-knapp när det finns mer
- Visar hur många som är kvar

---

## 🎨 GUI-layout:

```
┌─────────────────────────────────────────────────────────┐
│ 📋 Main Sheet Viewer                                    │
│ Visar alla länkar från main_sheet.xlsx (4829 rader)    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│ [Sök.....................] [Kolumn ▼] [🔍 Sök] [🔄 Visa alla]│
│                                                          │
│ Totalt: 4829 länkar | Visas: 100 | Unika kunder: 150   │
│                                                          │
│ ┌──────────────────────────────────────────────────┐   │
│ │ # │ Root │ Brand │ Pub URL │ Target │ Anchor ...│   │
│ ├──────────────────────────────────────────────────┤   │
│ │ 1 │ haxan.se │ ... │ ... │ ... │ Städprylar    │   │
│ │ 2 │ haxan.se │ ... │ ... │ ... │ Läs mer...    │   │
│ │ ... (scroll för mer)                             │   │
│ └──────────────────────────────────────────────────┘   │
│                                                          │
│ [Ladda fler (4729 kvar)]                                │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Teknisk implementation:

### **Backend (gui_app.py):**

**Ny endpoint:** `GET /api/mainsheet`

**Parameters:**
- `search` - Sökterm (valfri)
- `column` - Kolumn att söka i (valfri)
- `limit` - Antal rader per sida (default: 100)
- `offset` - Startposition (default: 0)

**Response:**
```json
{
  "records": [
    {
      "index": 0,
      "canonical_root": "haxan.se",
      "brand": "haxan.se",
      "pub_page_url": "https://...",
      "target_url": "https://...",
      "anchor_text": "Städprylar",
      "link_type": "Artikel",
      "language": "SE",
      "published_at": "2022-09-02"
    }
  ],
  "total": 4829,
  "filtered": 150,
  "unique_customers": 25,
  "showing": 100,
  "has_more": true
}
```

### **Frontend (templates/index.html + static/js/app.js):**

**Nya funktioner:**
- `loadMainSheet(append)` - Laddar data från API
- `searchMainSheet()` - Söker i data

**Features:**
- Sticky table header
- Scrollbar för många rader
- Klickbara URLs
- Hover-tooltips för långa URLs
- "Ladda fler"-knapp

---

## 🧪 Användning:

### **1. Öppna GUI:**
```
http://127.0.0.1:5000
```

### **2. Klicka på "📋 Main Sheet"-fliken**

### **3. Visa alla länkar:**
```
Klicka: "🔄 Visa alla"
→ Laddar första 100 rader
```

### **4. Sök efter kund:**
```
Skriv: "bethard"
Välj kolumn: "Canonical Root" (eller "Alla kolumner")
Klicka: "🔍 Sök"
→ Filtrerar alla rader som matchar
```

### **5. Sök efter ankartext:**
```
Skriv: "casino"
Välj kolumn: "Anchor Text"
Klicka: "🔍 Sök"
→ Hittar alla länkar med "casino" i ankartexten
```

### **6. Ladda fler:**
```
Scrolla ner
Klicka: "Ladda fler (X kvar)"
→ Laddar nästa 100 rader
```

---

## 📊 Exempel-användningsfall:

### **Use Case 1: Hitta alla länkar för en kund**
```
1. Gå till Main Sheet
2. Skriv: "bethard"
3. Välj: "Canonical Root"
4. Sök
→ Visar alla bethard.com länkar (t.ex. 56 st)
```

### **Use Case 2: Hitta länkar på specifik pub-domän**
```
1. Skriv: "kingsizemag.se"
2. Välj: "Pub URL"
3. Sök
→ Visar alla länkar publicerade på kingsizemag.se
```

### **Use Case 3: Hitta länkar med specifik ankartext**
```
1. Skriv: "betting"
2. Välj: "Anchor Text"
3. Sök
→ Visar alla länkar med "betting" i ankartexten
```

### **Use Case 4: Bläddra igenom alla länkar**
```
1. Klicka "Visa alla"
2. Scrolla genom tabellen
3. Klicka "Ladda fler" för nästa batch
→ Utforska alla 4829 länkar
```

---

## 🎨 Styling:

### **Tabell:**
- Sticky header (stannar synlig vid scroll)
- Zebra-striping för läsbarhet
- Hover-effekt på rader
- Max-width på URL-kolumner med ellipsis
- Tooltips för hela URL:er

### **Länkar:**
- Klickbara (öppnas i ny flik)
- Färgade med primärfärg
- Hover-underline

### **Responsiv:**
- Horisontell scroll för bred tabell
- Vertikal scroll för många rader (max 600px höjd)

---

## 🔍 Kolumner i tabellen:

| # | Kolumn | Innehåll |
|---|--------|----------|
| 1 | # | Radnummer (original index) |
| 2 | Canonical Root | Kunddomän (t.ex. haxan.se) |
| 3 | Brand | Brand-namn |
| 4 | Pub URL | Publiceringssida (URL där länken finns) |
| 5 | Target URL | Målsida (dit länken pekar) |
| 6 | Anchor Text | Ankartext |
| 7 | Type | Länktyp (Artikel, etc) |
| 8 | Published | Publiceringsdatum |

---

## 📈 Prestanda:

### **Optimeringar:**
- ✅ Paginering (100 rader/batch)
- ✅ Lazy loading ("Ladda fler")
- ✅ Server-side filtrering
- ✅ Effektiv pandas-läsning

### **Responstider:**
- Första laddning: ~1-2 sekunder
- Sökning: ~0.5-1 sekund
- Ladda fler: ~0.5 sekunder

---

## 💡 Tips:

### **Snabb sökning:**
```
1. Välj specifik kolumn (snabbare än "Alla kolumner")
2. Använd exakta termer
3. Kombinera med paginering för stora resultat
```

### **Export till CSV:**
```
Du kan redan nu:
1. Sök efter önskade länkar
2. Kopiera från tabellen
3. Klistra in i Excel

Framtida feature: Export-knapp
```

### **Keyboard shortcuts:**
```
Enter i sökfält = Sök
Ctrl+F i webbläsare = Hitta i synlig tabell
```

---

## 🐛 Troubleshooting:

### **Problem: "main_sheet.xlsx saknas"**
**Lösning:** 
```
Kontrollera att filen finns:
C:\Users\robin\PycharmProjects\linkdb\data\input\main_sheet.xlsx
```

### **Problem: Tabellen laddar inte**
**Lösning:**
```
1. Öppna Developer Tools (F12)
2. Kolla Console för fel
3. Verifiera att servern körs
4. Försök ladda om sidan (Ctrl+F5)
```

### **Problem: Sökresultat är tomma**
**Lösning:**
```
1. Kontrollera stavning
2. Prova "Alla kolumner" istället för specifik
3. Prova bredare sökterm (t.ex. "bet" istället för "bethard.com")
```

---

## 🎊 Sammanfattning:

**Main Sheet Viewer ger dig:**
- ✅ Fullständig översikt av alla 4829 länkar
- ✅ Kraftfull sökfunktion
- ✅ Filterering per kolumn
- ✅ Klickbara länkar för verifiering
- ✅ Statistik i realtid
- ✅ Snabb och responsiv

**Perfekt för:**
- 📊 Analysera länkportfölj
- 🔍 Hitta specifika länkar
- ✅ Verifiera pub-URLs
- 📈 Se historisk data
- 🎯 Identifiera patterns

---

## 📖 Relaterade filer:

- **Backend:** `gui_app.py` - `/api/mainsheet` endpoint
- **Frontend:** `templates/index.html` - Main Sheet tab
- **JavaScript:** `static/js/app.js` - loadMainSheet(), searchMainSheet()
- **Data:** `data/input/main_sheet.xlsx` - 4829 rader

---

**✅ Main Sheet Viewer är KLAR! Öppna http://127.0.0.1:5000 och klicka på "📋 Main Sheet"-fliken! 🚀**

