# LinkDB GUI - Testing Guide 🧪

**Complete guide för att testa LinkDB GUI applikationen**

Denna guide hjälper dig att komma igång och testa alla funktioner i LinkDB GUI-systemet.

---

## 📋 Förutsättningar

Innan du börjar, se till att du har:
- Python 3.8+ installerat
- Node.js 16+ installerat
- Git installerat
- En terminal/kommandorad

---

## 🚀 Snabbstart - Starta Applikationen

### Steg 1: Starta Backend (FastAPI)

Öppna en terminal och kör:

```bash
cd /home/user/LinkDB/gui/backend
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Vad händer:**
- FastAPI-servern startar på `http://localhost:8000`
- Du ser meddelande: "Application startup complete"
- AI routes laddas (med mock mode om ingen OpenAI API key finns)

**Verifiera:**
- Öppna `http://localhost:8000/health` i webbläsaren
- Du ska se: `{"status":"healthy","service":"LinkDB Analytics API"}`

### Steg 2: Starta Frontend (React)

Öppna EN NY terminal (behåll backend igång!) och kör:

```bash
cd /home/user/LinkDB/gui/frontend
npm run dev
```

**Vad händer:**
- Vite dev-server startar på `http://localhost:5173`
- Frontend kompileras
- Du ser: "Local: http://localhost:5173/"

**Öppna applikationen:**
- Gå till `http://localhost:5173` i din webbläsare
- LinkDB GUI ska nu laddas!

---

## 🎯 Komplett Test-Guide - Klicka Dig Runt!

### Test 1: Dashboard (Översikt)

**Steg:**
1. När du öppnar appen ska du se **Dashboard**
2. Titta på KPI-korten längst upp:
   - Total Customers
   - Total Links
   - Average Health (med cirkeldiagram)
3. Scrolla ner - se "Top Performers"-tabellen

**Vad att leta efter:**
- ✅ Alla nummer laddar korrekt
- ✅ Cirkeldiagrammet (Health Gauge) visar rätt poäng
- ✅ Inga console errors (högerklicka → Inspect → Console)

---

### Test 2: Customer List (Kundlista)

**Steg:**
1. Klicka på **"Customers"** i sidomenyn (vänster)
2. Du ska se en lista med alla kunder
3. Testa sökfunktionen:
   - Skriv ett kundnamn i sökfältet (t.ex. "bethard")
   - Listan filtreras automatiskt (debounced efter 300ms)
4. Klicka på EN kund i tabellen

**Vad att leta efter:**
- ✅ Alla kunder visas med data
- ✅ Sökning fungerar och filtrerar listan
- ✅ Badges visar status (Excellent/Good)
- ✅ När du klickar en kund → navigerar till Customer Analysis

---

### Test 3: Customer Analysis (Detaljerad Kundanalys)

**Steg:**
1. Du ska nu vara på en kund-sida (t.ex. `/customers/1`)
2. Överst ser du:
   - Kundens namn och brand
   - Overall Health badge + Health Gauge
3. Testa att växla mellan tabs:
   - **Overview**: Länkportfolio, rekommendationer, AI-insikter (scroll ner!)
   - **Anchor Analysis**: Ankartextanalys med pie chart
   - **Temporal Patterns**: Temporal distribution med bar chart
   - **Domain Quality**: TLD-distribution
   - **Competitive**: Coming soon-meddelande
   - **🤖 AI Assistant**: AI chat-gränssnitt!

**Vad att leta efter:**
- ✅ Alla tabs laddar utan error
- ✅ Charts renderas korrekt (pie chart, bar charts)
- ✅ AI Insights-panelen visar 5 insikter längst ner på Overview
- ✅ Recommendations-kortet visar 3 rekommendationer med prioritet
- ✅ AI Assistant-tabben visar en chat-interface

---

### Test 4: AI-Funktioner (AI Intelligence) 🤖

#### A. AI Insights på Customer Analysis

**Steg:**
1. Gå till en kund (t.ex. `/customers/1`)
2. Se till att du är på **Overview**-tabben
3. Scrolla ner till "AI-Genererade Insikter"-panelen (blå kort)
4. Du ska se 5 AI-genererade insikter baserat på kundens data

**Vad att leta efter:**
- ✅ 5 insikter visas med numrering (1-5)
- ✅ Varje insikt är specifik för kundens data
- ✅ Insikterna innehåller emojis (🌟, ✅, ⚠️, etc.)

#### B. AI Recommendations

**Steg:**
1. På samma sida, titta på "Smarta Rekommendationer" (gröna kort)
2. Du ska se 3 prioriterade rekommendationer
3. Varje rekommendation har:
   - Prioritet (1, 2, 3)
   - Titel
   - Åtgärd
   - Reasoning
   - Impact badge (HIGH, MEDIUM, LOW)

**Vad att leta efter:**
- ✅ 3 rekommendationer visas
- ✅ Badges visar impact level
- ✅ Åtgärder är konkreta och actionable

#### C. AI Chat (I Customer Analysis)

**Steg:**
1. Klicka på **"🤖 AI Assistant"**-tabben
2. Du ska se en ChatGPT-liknande chat-interface
3. Testa snabbfrågorna (knappar längst ner):
   - Klicka "Hur ser min länkprofil ut?"
   - AI svarar med kundspecifik analys
4. Testa att skriva egna frågor:
   - "Vilka risker har jag?"
   - "Vad ska jag göra härnäst?"
   - "Analysera min ankartextstrategi"

**Vad att leta efter:**
- ✅ AI svarar inom 1-2 sekunder
- ✅ Svaren är relevanta och SEO-fokuserade
- ✅ Chat-bubblor visar user (blå) och assistant (grå)
- ✅ Scroll fungerar automatiskt till senaste meddelande

#### D. Dedikerad AI Chat-sida

**Steg:**
1. Klicka på **"AI Assistant"**-knappen i headern (blå-lila gradient-knapp längst upp)
2. Du navigeras till `/ai-chat`
3. Du ser en fullsize AI chat-sida med:
   - Titel med gradient
   - Beskrivning
   - Chat-interface
   - 3 feature-kort (Dataanalys, Strategiråd, Riskdetektering)
4. Testa chatten igen:
   - Skriv "Ge mig en översikt av alla mina kunder"
   - Skriv "Vad är den viktigaste risken att vara medveten om?"

**Vad att leta efter:**
- ✅ Gradient-titel renderas korrekt
- ✅ Feature-korten ser snygga ut med gradients
- ✅ AI chat fungerar lika bra som i Customer Analysis
- ✅ Snabbfrågorna fyller i input-fältet

---

### Test 5: Competitive Benchmarking

**Steg:**
1. Klicka på **"Competitive"** i sidomenyn
2. Du ska se:
   - Industry KPIs (4 kort)
   - Scatter plot (Customer Distribution)
   - Top 10 by Volume
   - Top 10 by Quality

**Vad att leta efter:**
- ✅ KPIs visar siffror
- ✅ Scatter plot renderas (kan vara tom om ingen data)
- ✅ Top 10-listor fylls med data

---

### Test 6: Link Explorer

**Steg:**
1. Klicka på **"Links"** i sidomenyn
2. Du ska se:
   - Sökfält + Export-knappar
   - Tabell med länkar
   - Pagination (Previous/Next)
3. Testa sökning:
   - Skriv ett domännamn
   - Tabellen filtreras
4. Testa export:
   - Klicka **"Export CSV"**
   - En CSV-fil laddar ner
   - Klicka **"Export JSON"**
   - En JSON-fil laddar ner
5. Testa pagination:
   - Klicka "Next" för nästa sida
   - Klicka "Previous" för att gå tillbaka

**Vad att leta efter:**
- ✅ Länkar visas i tabell
- ✅ Sökning fungerar (debounced efter 500ms)
- ✅ CSV export skapar en .csv-fil
- ✅ JSON export skapar en .json-fil
- ✅ Pagination fungerar om det finns många länkar
- ✅ Datum formateras korrekt (svensk locale)

---

### Test 7: Settings

**Steg:**
1. Klicka på **"Settings"** i sidomenyn
2. Du ska se en settings-sida

**Vad att leta efter:**
- ✅ Sidan renderas utan errors

---

## 🐛 Vanliga Problem & Lösningar

### Problem 1: Backend startar inte

**Symptom:** `ModuleNotFoundError` eller liknande

**Lösning:**
```bash
cd gui/backend
pip install -r requirements.txt
```

### Problem 2: Frontend visar tomma kort

**Symptom:** KPIs visar 0 eller "N/A"

**Lösning:**
- Kontrollera att backend körs på port 8000
- Öppna browser console (F12) och leta efter CORS errors
- Verifiera att `http://localhost:8000/health` fungerar

### Problem 3: AI funktioner visar inte data

**Symptom:** AI Insights eller Recommendations är tomma

**Lösning:**
- Detta är NORMALT om databasen är tom
- AI-servicen använder intelligent mock mode
- Om du har en OpenAI API key, sätt:
  ```bash
  export OPENAI_API_KEY="sk-..."
  ```

### Problem 4: Charts renderas inte

**Symptom:** Tomma områden där charts ska vara

**Lösning:**
- Öppna browser console och leta efter errors
- Verifiera att data finns i network tab (F12 → Network → XHR)
- Recharts kräver valid data - om data är `null`, renderas ingenting

### Problem 5: Build failures

**Symptom:** `npm run build` failar

**Lösning:**
```bash
cd gui/frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

---

## ✅ Checklist - Allt Som Ska Fungera

Använd denna checklist för att verifiera att allt fungerar:

### Backend
- [ ] Backend startar utan errors på port 8000
- [ ] `/health` endpoint svarar
- [ ] `/api/customers` returnerar data
- [ ] `/api/dashboard/metrics` returnerar data
- [ ] `/api/ai/chat` svarar (även utan API key)
- [ ] `/api/ai/insights/1` returnerar insikter
- [ ] `/api/ai/recommendations/1` returnerar rekommendationer

### Frontend - Core
- [ ] Frontend startar på port 5173
- [ ] Dashboard laddar utan errors
- [ ] Sidebar navigation fungerar
- [ ] Header visar AI Assistant-knapp
- [ ] Alla sidor är accessible via navigation

### Frontend - Pages
- [ ] Dashboard visar KPIs och charts
- [ ] Customer List visar alla kunder
- [ ] Customer List sökning fungerar
- [ ] Customer Analysis har 6 tabs (inkl AI)
- [ ] Alla charts renderas (Health Gauge, Pie, Bar)
- [ ] Competitive Benchmarking visar data
- [ ] Link Explorer visar tabell med länkar
- [ ] Link Explorer export fungerar (CSV + JSON)
- [ ] AI Chat-sidan fungerar

### Frontend - AI Features
- [ ] AI Insights visas på Customer Analysis (Overview)
- [ ] AI Recommendations visas på Customer Analysis (Overview)
- [ ] AI Assistant tab fungerar i Customer Analysis
- [ ] AI Chat-knapp i header navigerar till /ai-chat
- [ ] AI chat svarar på frågor
- [ ] Snabbfrågor fyller i input
- [ ] Chat scrollar automatiskt

### Frontend - UX
- [ ] Loading spinners visas vid laddning
- [ ] Empty states visas när ingen data
- [ ] Error meddelanden visas vid fel
- [ ] Hover-effekter fungerar på knappar
- [ ] Responsive design (prova resize window)
- [ ] Lazy loading fungerar (no flash of all content)

---

## 🎯 Advanced Testing

### Performance Testing

1. **Öppna DevTools Performance Tab**
   - F12 → Performance
   - Start recording
   - Navigera mellan sidor
   - Stop recording
   - Kontrollera: First Contentful Paint < 2s

2. **Network Testing**
   - F12 → Network
   - Disable cache
   - Reload sidan
   - Kontrollera: Total load time < 3s

3. **Bundle Size**
   ```bash
   cd gui/frontend
   npm run build
   ```
   - Kontrollera: Gzipped bundle < 200 kB

### Accessibility Testing

1. **Keyboard Navigation**
   - Tryck Tab-tangenten genom hela appen
   - Alla interaktiva element ska vara nåbara
   - Enter ska aktivera knappar

2. **Screen Reader**
   - Mac: VoiceOver (Cmd + F5)
   - Windows: Narrator (Win + Ctrl + Enter)
   - Navigera genom appen - allt ska läsas upp

---

## 📊 Expected Data

Om databasen innehåller exempel-data, förvänta dig:

- **Customers:** 5-10 kunder
- **Links per customer:** 20-60 länkar
- **Overall health scores:** 60-85/100
- **AI Insights:** 5 per kund
- **AI Recommendations:** 3 per kund

---

## 🆘 Få Hjälp

Om något inte fungerar:

1. **Kolla console errors** (F12 → Console)
2. **Kolla network requests** (F12 → Network)
3. **Kolla backend logs** (terminal där uvicorn körs)
4. **Sök efter error-meddelanden** i denna guide

---

## 🎉 Framgång!

Om alla tests passerar:
- ✅ **Backend fungerar:** FastAPI serverar data korrekt
- ✅ **Frontend fungerar:** React-appen renderar perfekt
- ✅ **AI fungerar:** Intelligent mock mode eller real OpenAI
- ✅ **Integration fungerar:** Frontend ↔ Backend kommunicerar
- ✅ **UX fungerar:** Smooth, responsive, professional

**Grattis! LinkDB GUI är deployment-ready!** 🚀

---

**Version:** 1.0.0
**Datum:** 2025-11-12
**Tracks:** 1-6 Complete
**Status:** ✅ Production Ready
