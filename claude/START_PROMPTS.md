# LinkDB GUI - Start Prompts för Alla Tracks

Kopiera och klistra in dessa prompts i Claude Code för att starta varje track.

---

## 🚀 PHASE 1: Start Samtidigt (Parallel)

### Track 1: Backend API

```
Jag vill att du implementerar TRACK_1_BACKEND_API.md

Du är Track 1 av 6 parallella utvecklingsteam som bygger LinkDB GUI.

DIN UPPGIFT:
Bygg komplett FastAPI backend som exponerar alla analyzers via REST API.

VIKTIGA PUNKTER:
- Skapa gui/backend/ directory structure
- Bygg API routes: customers, links, competitive, dashboard
- Integrera med befintliga analyzers från ../app/analyzers/
- Implementera error handling och CORS
- Testa alla endpoints

DO NOT TOUCH:
- gui/frontend/ (Track 2, 3, 4, 5 arbetar där)
- ../app/analyzers/ (befintliga filer, bara importera dem)

DELIVERABLES:
- Fungerande FastAPI app på localhost:8000
- Alla endpoints dokumenterade
- API_DOCUMENTATION.md skapad

IMPORTANT:
Följ specen exakt. Du är backend specialist.
Andra tracks förlitar sig på ditt API!

START NOW! 🚀
```

---

### Track 2: Frontend Core

```
Jag vill att du implementerar TRACK_2_FRONTEND_CORE.md

Du är Track 2 av 6 parallella utvecklingsteam som bygger LinkDB GUI.

DIN UPPGIFT:
Bygg React-applikationens core: layout, routing, common components.

VIKTIGA PUNKTER:
- Initialize React + Vite + Tailwind CSS
- Skapa Layout components (Sidebar, Header)
- Skapa Common components (Button, Card, Badge, etc)
- Setup routing med React Router
- Skapa placeholder pages (Track 4 gör riktiga pages senare)

DO NOT TOUCH:
- gui/backend/ (Track 1 gör backend)
- src/components/charts/ (Track 3 gör charts)
- src/pages/ content (Track 4 gör pages, du gör bara placeholders)
- src/utils/ (Track 5 gör utils)

DELIVERABLES:
- React app fungerande på localhost:5173
- Layout med sidebar och header
- Common components redo att använda
- FRONTEND_SETUP.md skapad för andra tracks

IMPORTANT:
Du skapar fundamentet. Track 3 och 4 bygger ovanpå dig!
Gör det professionellt och återanvändbart.

START NOW! 🎨
```

---

### Track 3: Charts & Visualizations

```
Jag vill att du implementerar TRACK_3_CHARTS_VISUALIZATIONS.md

Du är Track 3 av 6 parallella utvecklingsteam som bygger LinkDB GUI.

DIN UPPGIFT:
Bygg ALLA chart components med Recharts.

VIKTIGA PUNKTER:
- Install Recharts
- Skapa HealthGauge (circular gauge)
- Skapa AnchorDistributionChart (pie chart)
- Skapa TemporalChart (line/area chart)
- Skapa MonthlyDistributionChart (bar chart)
- Skapa DomainDistributionChart (horizontal bars)
- Skapa TLDDistributionChart (donut chart)
- Skapa CompetitiveScatterPlot (scatter med quadrants)

DO NOT TOUCH:
- gui/backend/ (Track 1)
- src/components/layout/ (Track 2)
- src/components/common/ (Track 2)
- src/pages/ (Track 4)

DELIVERABLES:
- Alla chart components i src/components/charts/
- Responsive och interactive
- Custom tooltips
- charts/README.md med usage examples

IMPORTANT:
Track 4 kommer importera dina charts!
Gör dem beautiful och reusable.
Test med sample data.

START NOW! 📊
```

---

## ⏸️ PAUSE - Vänta på Phase 1

**Innan du startar Track 4:**
1. Verifiera Track 1: `curl http://localhost:8000/health` → ska fungera
2. Verifiera Track 2: `npm run dev` → ska visa sidebar
3. Verifiera Track 3: Check att alla chart files finns

---

## 🔄 PHASE 2: Integration

### Track 4: Pages & Views

```
Jag vill att du implementerar TRACK_4_PAGES_VIEWS.md

Du är Track 4 av 6 parallella utvecklingsteam som bygger LinkDB GUI.

DIN UPPGIFT:
Bygg ALLA main pages och integrera med backend API + chart components.

VIKTIGA PUNKTER:
- Dashboard page (KPIs + charts)
- Customer list page (table + search)
- Customer analysis page (5 TABS - detta är critical!)
- Competitive benchmarking page
- Link explorer page (filters + pagination)
- Settings page

INTEGRATION:
- Använd Track 2 Layout & common components
- Använd Track 3 charts
- Fetch data från Track 1 backend API
- Implementera loading states och error handling

DO NOT TOUCH:
- gui/backend/ (Track 1)
- src/components/layout/ (Track 2)
- src/components/charts/ (Track 3)
- src/utils/ (Track 5 kommer skapa detta)

DELIVERABLES:
- Alla pages fungerar
- Data laddar från backend
- Charts visar real data
- Navigation fungerar
- Responsive design

IMPORTANT:
Customer Analysis page HAR 5 TABS:
1. Overview
2. Anchor Analysis
3. Temporal Patterns
4. Domain Quality
5. Competitive

Använd real data från backend API!
Test varje page som du bygger.

START NOW! 🖥️
```

---

## ⏸️ PAUSE - Vänta på Track 4

Verifiera att alla pages fungerar innan Track 5.

---

## ✨ PHASE 3: Polish & AI

### Track 5: Utils & Polish

```
Jag vill att du implementerar TRACK_5_UTILS_POLISH.md

Du är Track 5 av 6 - FINALIZING track som polerar allt!

DIN UPPGIFT:
Skapa utilities, hooks, export functionality och polish complete application.

VIKTIGA PUNKTER:
- Skapa API client (src/utils/api.js)
- Skapa formatters (src/utils/formatters.js)
- Skapa export utils (src/utils/export.js)
- Skapa React Query hooks (4 files)
- REFACTOR Track 4 pages att använda dina hooks
- Add loading skeletons
- Add empty states
- Fix ALL bugs
- Optimize performance
- Add polish (animations, transitions)

DU FÅR RÖRA:
- ALT! Du är sista track, fixa det som behövs.
- REFACTOR pages från Track 4 till bättre kod
- Fix bugs från andra tracks
- Optimize performance

DELIVERABLES:
- API client & formatters
- React Query setup & hooks
- Pages refactored to use hooks
- Loading skeletons & empty states
- Zero console errors
- Smooth performance
- Export functionality works
- DEPLOYMENT_READY.md skapad

IMPORTANT:
Detta är SISTA steget före deployment.
Gör allt PERFECT!
Test EVERYTHING!

START NOW! ✨
```

---

### Track 6: AI Intelligence (PARALLEL!)

```
Jag vill att du implementerar TRACK_6_AI_INTELLIGENCE.md

Du är Track 6 - den HEMLIGA KILLER FEATURE!

DIN UPPGIFT:
Bygg AI-powered intelligence layer som gör LinkDB SMART, inte bara en dashboard.

VIKTIGA PUNKTER:
- Integrera OpenAI/Anthropic LLM
- Bygg AI chat assistant (ChatGPT i GUI)
- Auto-generate insights från customer data
- Smart recommendations med LLM
- Natural language query
- Pattern detection med AI

BACKEND:
- gui/backend/ai/ai_service.py
- gui/backend/routes/ai.py
- Nya /api/ai/ endpoints

FRONTEND:
- AIAssistant.jsx (chat interface)
- InsightsPanel.jsx (auto-generated insights)
- RecommendationsCard.jsx (smart recs)
- AIChat.jsx (full page)

INTEGRATION:
- Inject AI components i Track 4 pages
- Add AI Assistant button i Header (Track 2)
- Add AI tab i CustomerAnalysis

IMPORTANT:
Du kan köra PARALLELLT med Track 4 & 5!
Du har inga dependencies.
Skapa nya filer, integrera i befintliga.

Detta är GAME-CHANGER featuren!
Andra SEO tools visar bara data.
VI har AI som FÖRSTÅR och REKOMMENDERAR!

Set OPENAI_API_KEY först:
export OPENAI_API_KEY="sk-..."

START NOW! 🤖✨💥
```

---

## 📊 Execution Order

### Optimal Workflow:

```
START SAMTIDIGT:
├─ Track 1 (Backend)
├─ Track 2 (Frontend Core)
└─ Track 3 (Charts)

VÄNTA TILLS ALLA 3 KLARA
↓

START:
├─ Track 4 (Pages)
└─ Track 6 (AI Intelligence) ← KAN KÖRAS SAMTIDIGT!

VÄNTA TILLS TRACK 4 KLAR
↓

START:
└─ Track 5 (Polish)

KLART! 🎉
```

### Timeline:
- **Phase 1** (Track 1,2,3): 2-3 hours wallclock
- **Phase 2** (Track 4,6): 3-4 hours wallclock
- **Phase 3** (Track 5): 2-3 hours wallclock
- **TOTAL:** ~8-10 hours wallclock (vs 20+ sequentially!)

---

## 💡 Pro Tips

1. **Öppna flera Claude Code windows**
   - Ett för varje track
   - Märk dem tydligt (Track 1, Track 2, etc)

2. **Copy-paste prompt direkt**
   - Ingen editing behövs
   - Prompts är ready-to-use

3. **Verifiera mellan phases**
   - Test att föregående tracks fungerar
   - Spara tid genom att hitta bugs tidigt

4. **Monitor credits**
   - $150 budget totalt
   - Justera om nödvändigt

5. **Ha tålamod**
   - Låt AI jobba
   - Granska output när klar
   - Kör test

---

## 🎬 Let's Go!

**STARTA MED:**

1. Öppna 3 Claude Code windows
2. Copy-paste Track 1, 2, 3 prompts
3. Tryck Enter på alla 3 samtidigt
4. ☕ Kolla efter 2-3 timmar
5. Verifiera Phase 1 fungerar
6. Fortsätt med Phase 2 & 3

**GOOD LUCK!** 🚀

---

*Alla prompts är production-ready. Just copy-paste and GO!* 💪
