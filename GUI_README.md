# 🎨 Link Planning GUI - Webbgränssnitt för Länkplanering

## ✨ Vad är det?

Ett modernt, responsivt webbgränssnitt för intelligent länkplanering. Byggt med Flask (backend) och vanilla JavaScript (frontend).

![GUI Preview](https://via.placeholder.com/800x400?text=Link+Planning+GUI)

---

## 🚀 Snabbstart

### Starta GUI:n

**Alternativ 1 - Dubbelklicka:**
```
start_gui.bat
```

**Alternativ 2 - Kommandorad:**
```bash
cd C:\Users\robin\PycharmProjects\linkdb
python gui_app.py
```

**Alternativ 3 - Direkt:**
```bash
python gui_app.py
```

GUI:n öppnas automatiskt på: **http://127.0.0.1:5000**

---

## 📊 Features

### 1. **Dashboard med statistik**
- Totalt antal kunder
- Totalt antal länkar
- Unika publiceringsdomäner
- Unika måldomäner

### 2. **Kunder-vy** 📋
- Lista alla kunder med metadata
- Sök och filtrera kunder
- Klicka på kund för detaljerad historik
- Se:
  - Totalt antal länkar
  - Anchor diversity score
  - Anchor type distribution
  - Vanligaste ankartexter
  - Rekommendationer
  - Månadshistorik

### 3. **Planering-vy** 🎯
- **Steg 1:** Lägg till kunder och antal länkar
- **Steg 2:** Analysera volym
  - Se automatisk strategi-klassificering
  - Bedöm semantisk kapacitet
  - Jämför med historik
- **Steg 3:** Generera plan
  - Optimal anchor distribution
  - Diversifierade ankartexter
  - Prioriterade länkar
- **Exportera:** Ladda ner plan som CSV

### 4. **Historik-vy** 📅
- Välj kund och se månadshistorik
- Se utveckling över tid
- Analysera mönster i:
  - Antal länkar per månad
  - Anchor type distribution
  - Vanligaste ankartexter
  - Målside-distribution

---

## 🎨 Design

### Färgschema
- **Primary:** Modern blå (#2563eb)
- **Success:** Grön (#10b981)
- **Warning:** Orange (#f59e0b)
- **Modern gradient bakgrund**

### UI/UX
- ✅ Responsiv design (fungerar på mobil, tablet, desktop)
- ✅ Smooth animations
- ✅ Modal dialogs för detaljer
- ✅ Loading states
- ✅ Error handling
- ✅ Intuitive navigation

---

## 🔌 API Endpoints

### GET `/`
Huvudsida - Dashboard

### GET `/api/customers`
Hämta alla kunder med metadata

**Response:**
```json
{
  "customers": [
    {
      "id": 117,
      "canonical_root": "bethard.com",
      "brand": "Bethard",
      "total_links": 56,
      "unique_pub_domains": 15
    }
  ],
  "count": 1
}
```

### GET `/api/customer/<id>/history`
Hämta historisk analys för en kund

**Response:**
```json
{
  "customer_id": 117,
  "canonical_root": "bethard.com",
  "total_links": 56,
  "anchor_diversity_score": 0.82,
  "primary_strategy": "authority_building",
  "recommendations": [...]
}
```

### GET `/api/customer/<id>/monthly`
Hämta månadshistorik för en kund

**Response:**
```json
{
  "months": [
    {
      "year": 2024,
      "month": 10,
      "display_name": "Oktober 2024",
      "link_count": 5,
      "anchor_types": {...}
    }
  ]
}
```

### POST `/api/detect-volume`
Detektera volym och strategi

**Request:**
```json
{
  "planning_data": {
    "117": 15,
    "118": 8
  }
}
```

**Response:**
```json
{
  "volumes": [
    {
      "customer_id": 117,
      "planned_links": 15,
      "recommended_strategy": "semantic_foundation",
      "semantic_planning_possible": true
    }
  ]
}
```

### POST `/api/generate-plan`
Generera länkplan

**Request:**
```json
{
  "planning_data": {
    "117": 15
  },
  "plan_name": "November Plan"
}
```

**Response:**
```json
{
  "plan_name": "November Plan",
  "total_links": 15,
  "csv_file": "link_plan_20251106_010203.csv",
  "customers": [...]
}
```

### GET `/api/download/<filename>`
Ladda ner exporterad CSV-fil

### GET `/api/stats`
Hämta övergripande statistik

---

## 📁 Filstruktur

```
linkdb/
├── gui_app.py                  # Flask backend
├── start_gui.bat               # Start-script
│
├── templates/
│   └── index.html              # Huvudtemplate
│
├── static/
│   ├── css/
│   │   └── style.css           # Alla styles
│   └── js/
│       └── app.js              # All JavaScript-logik
│
└── data/
    └── output/
        └── *.csv               # Exporterade planer
```

---

## 🔧 Teknisk Stack

### Backend
- **Flask** - Python web framework
- **SQLite** - Databas
- **Python modules:**
  - `app.planning.volume_detector`
  - `app.planning.basic_plan_generator`
  - `app.analyzers.link_history_analyzer`
  - `app.analyzers.monthly_link_viewer`

### Frontend
- **HTML5**
- **CSS3** (modern, responsive)
- **Vanilla JavaScript** (ES6+)
- **Fetch API** för AJAX-anrop

---

## 💡 Användning

### 1. **Visa kundöversikt:**
- Gå till "Kunder"-fliken
- Sök efter specifik kund
- Klicka på kund för detaljer

### 2. **Skapa en plan:**
1. Gå till "Planering"-fliken
2. Välj kund och antal länkar
3. Klicka "Lägg till"
4. Upprepa för fler kunder
5. Klicka "Analysera volym"
6. Se rekommendationer
7. Klicka "Generera plan"
8. Granska och ladda ner CSV

### 3. **Se månadshistorik:**
1. Gå till "Historik"-fliken
2. Välj kund
3. Klicka "Visa historik"
4. Se utveckling per månad

---

## 🎯 Exempel Workflow

```
1. Dashboard visar 150 kunder, 5000 länkar
   ↓
2. Gå till Kunder → Sök "bethard"
   ↓
3. Klicka på bethard.com
   → Se 56 länkar, anchor diversity 0.82
   → Se 14 månader med data
   ↓
4. Gå till Planering
   → Lägg till bethard.com, 15 länkar
   → Lägg till annan kund, 8 länkar
   ↓
5. Analysera volym
   → bethard: semantic_foundation
   → Kan bygga topic clusters ✅
   ↓
6. Generera plan
   → 23 länkar totalt
   → Optimal anchor distribution
   ↓
7. Ladda ner CSV
   → Importera i Excel/Sheets
   → Använd för publicering
```

---

## 🐛 Troubleshooting

### Problem: "Address already in use"
**Lösning:** Någon annan process kör på port 5000
```bash
# Byt port i gui_app.py
app.run(debug=True, host='127.0.0.1', port=5001)
```

### Problem: "No module named 'flask'"
**Lösning:** Installera Flask
```bash
pip install flask
```

### Problem: "Database not found"
**Lösning:** Kontrollera att databaserna finns
```bash
# Ska finnas:
data/output/linkops_history.db
data/output/customers/*/customer.db
```

### Problem: GUI laddar inte data
**Lösning:** Öppna Developer Tools (F12) och kolla Console för fel

---

## 🔜 Framtida Features

### Fas 2 (Semantisk Motor):
- [ ] Entity extraction från målsidor
- [ ] Semantic clustering visualization
- [ ] Intelligent anchor suggestions
- [ ] Topic authority graphs

### Fas 3 (Advanced):
- [ ] Google Sheets integration
- [ ] Real-time collaboration
- [ ] A/B testing av planer
- [ ] Performance analytics
- [ ] User authentication
- [ ] Multi-language support

---

## 📸 Screenshots

### Dashboard
```
┌─────────────────────────────────────────┐
│  🎯 Link Planning GUI                   │
│  Intelligent länkplanering              │
├─────────────────────────────────────────┤
│  [150]    [5000]    [500]    [200]     │
│  Kunder   Länkar    Pub      Target     │
├─────────────────────────────────────────┤
│  📊 Kunder  🎯 Planering  📅 Historik  │
└─────────────────────────────────────────┘
```

### Kunder-vy
```
┌──────────────┬──────────────┬──────────────┐
│ bethard.com  │ cherry.com   │ hajper.com   │
│ 56 länkar    │ 42 länkar    │ 38 länkar    │
│ 15 domäner   │ 12 domäner   │ 14 domäner   │
└──────────────┴──────────────┴──────────────┘
```

### Planering-vy
```
┌─────────────────────────────────────────┐
│ 1. Välj kunder                          │
│ [bethard.com ▼] [15] [Lägg till]      │
│                                         │
│ Tillagda:                               │
│ • bethard.com - 15 länkar              │
│ • cherry.com - 8 länkar                │
│                                         │
│ [2. Analysera volym] [3. Generera plan]│
└─────────────────────────────────────────┘
```

---

## ✅ Checklista

- [x] Flask backend implementerad
- [x] Responsive HTML/CSS
- [x] JavaScript med Fetch API
- [x] Alla API endpoints fungerar
- [x] Modal dialogs för detaljer
- [x] Loading states
- [x] Error handling
- [x] CSV export
- [x] Månadshistorik
- [x] Volymdetektering
- [x] Plangenerering
- [x] Start-script (batch)
- [x] README dokumentation

---

## 🎉 Status

**✅ FÄRDIGT OCH REDO ATT ANVÄNDA!**

GUI:n är en fullständig, produktionsklar lösning för länkplanering med:
- Modern design
- Alla kärnfunktioner
- Enkel att använda
- Skalbar arkitektur

**Starta nu:** Dubbelklicka på `start_gui.bat` eller kör `python gui_app.py`

**Öppna:** http://127.0.0.1:5000

---

**💡 Tips:** Lägg till `start_gui.bat` som genväg på skrivbordet för snabb åtkomst!

