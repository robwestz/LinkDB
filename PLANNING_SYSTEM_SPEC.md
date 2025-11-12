# Intelligent Link Planning System - Projektplan

## Vision
Ett AI-drivet system som automatiskt planerar länkar baserat på semantisk SEO, topical authority och historisk länkdata för att maximera SEO-värde genom strategisk länkplanering.

## Problem att lösa
1. **Manuell planering är tidskrävande** - Varje länk planeras individuellt
2. **Saknar sammanhang** - Länkar planeras utan att se helheten
3. **Ineffektiv SEO** - Länkar stärker inte varandra semantiskt
4. **Ingen datadrivning** - Historik och resultat används inte i planeringen
5. **Skalbarhet** - Svårt att planera många länkar samtidigt

## Lösning
Ett system som:
- **Analyserar länkhistorik** för att identifiera mönster och framgång
- **Grupperar kunder** baserat på antal tillgängliga länkar
- **Planerar semantiskt** genom att hitta relaterade sökfraser och entiteter
- **Bygger topical authority** genom att länka strategiskt till relaterade sidor
- **Optimerar ankartexter** för att stärka specifika entiteter
- **Automatiserar processen** från analys till färdig plan

---

## Arkitektur - Moduler

### 1. **Link History Analyzer** 
Analyserar befintlig länkhistorik för att hitta mönster.

**Input:**
- `links_history` från databas
- Customer_id

**Output:**
- Använd länkstrategi (vilka ankartexter fungerar bäst)
- Populära målsidor
- Länkfrekvens per period
- Performance metrics

**Filer:**
- `app/analyzers/link_history_analyzer.py`

---

### 2. **Customer Grouping Engine**
Grupperar kunder baserat på antal tillgängliga länkar.

**Logik:**
```
Räkna rader per customer_id i planeringsdokument
→ Gruppera (1 länk, 2-5 länkar, 6-10 länkar, 11+ länkar)
→ Olika strategier per grupp
```

**Output:**
- Customer groups med metadata
- Rekommenderad strategi per grupp

**Filer:**
- `app/planning/customer_grouper.py`

---

### 3. **Semantic SEO Engine** 🧠
Hjärtat i systemet - bygger semantiska relationer.

**Funktioner:**
- **Entity extraction** - Hitta huvudentiteter på målsidor
- **Related phrase finder** - Hitta semantiskt relaterade sökfraser
- **Topical clustering** - Gruppera sidor i topics
- **Authority building** - Planera länkar för att bygga authority inom ett topic

**Input:**
- Målsidor (URLs)
- Antal tillgängliga länkar
- Kundens nisch/bransch

**Output:**
- Semantic clusters (grupper av relaterade sidor)
- Rekommenderade ankartexter per sida
- Link distribution plan

**Tekniker:**
- NLP för textanalys
- TF-IDF för nyckelordsviktning
- Word embeddings för semantisk likhet
- Topic modeling (LDA/NMF)

**Filer:**
- `app/semantic/entity_extractor.py`
- `app/semantic/phrase_finder.py`
- `app/semantic/topic_clusterer.py`
- `app/semantic/authority_builder.py`

---

### 4. **Anchor Text Optimizer**
Genererar och optimerar ankartexter.

**Strategier:**
- **Exact match** (10-20%) - Exakt sökfras
- **Partial match** (30-40%) - Delar av sökfras
- **Branded** (20-30%) - Varumärke
- **Generic** (20-30%) - Allmänna texter (klicka här, läs mer)
- **LSI keywords** (10-20%) - Semantiskt relaterade fraser

**Output:**
- Diversifierade ankartexter
- Naturlig distribution
- SEO-optimerad mix

**Filer:**
- `app/planning/anchor_optimizer.py`

---

### 5. **Planning Generator**
Skapar den slutliga planen.

**Process:**
```
1. Analysera historik
2. Gruppera kunder
3. För varje kund:
   a. Hämta målsidor från planeringsdokument
   b. Extrahera entiteter från målsidor
   c. Hitta semantiska relationer
   d. Skapa topic clusters
   e. Distribuera länkar strategiskt
   f. Generera ankartexter
4. Exportera plan
```

**Output:**
- Färdig länkplan (CSV/Excel)
- Kolumner:
  - customer_id
  - canonical_root
  - target_url
  - anchor_text
  - anchor_type
  - semantic_cluster
  - topic
  - priority_score
  - reasoning (varför denna länk/ankar)

**Filer:**
- `app/planning/plan_generator.py`

---

### 6. **Planning Document Manager**
Hanterar kommunikation med Google Sheets planeringsdokument.

**Funktioner:**
- Läs planeringsdokument
- Identifiera customer_id och antal länkar
- Hämta målsidor
- Skriv tillbaka planer
- Validera data

**Filer:**
- `app/integration/sheets_manager.py`

---

## Dataflöde

```
┌─────────────────────────────────────────────────────────────┐
│ 1. LÄSA PLANERINGSDOKUMENT (Google Sheets)                  │
│    → Få customer_id, antal rader, målsidor                  │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. ANALYSERA HISTORIK (Link History Analyzer)               │
│    → Se vad som fungerat tidigare för kunden                │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. GRUPPERA KUNDER (Customer Grouper)                       │
│    → Olika strategier baserat på antal länkar               │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. SEMANTISK ANALYS (Semantic SEO Engine)                   │
│    → Extrahera entiteter från målsidor                      │
│    → Hitta relaterade fraser                                │
│    → Skapa topic clusters                                   │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. OPTIMERA ANKARTEXTER (Anchor Optimizer)                  │
│    → Generera diversifierade ankartexter                    │
│    → Följ naturlig distribution                             │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. GENERERA PLAN (Planning Generator)                       │
│    → Kombinera allt till färdig plan                        │
│    → Exportera till CSV/Sheets                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Databas Schema - Nya tabeller

### `link_plans` - Färdiga planer
```sql
CREATE TABLE link_plans (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL REFERENCES customers(id),
  plan_name TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  status TEXT DEFAULT 'draft', -- draft, approved, executed
  total_links INTEGER,
  semantic_strategy TEXT
);
```

### `planned_links` - Individuella länkningar i planen
```sql
CREATE TABLE planned_links (
  id INTEGER PRIMARY KEY,
  plan_id INTEGER NOT NULL REFERENCES link_plans(id),
  customer_id INTEGER NOT NULL,
  target_url TEXT NOT NULL,
  anchor_text TEXT NOT NULL,
  anchor_type TEXT, -- exact, partial, branded, generic, lsi
  semantic_cluster TEXT,
  topic TEXT,
  priority_score REAL DEFAULT 0,
  reasoning TEXT, -- Förklaring av valet
  status TEXT DEFAULT 'planned', -- planned, published, cancelled
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### `semantic_clusters` - Semantiska grupperingar
```sql
CREATE TABLE semantic_clusters (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  cluster_name TEXT NOT NULL,
  topic TEXT,
  keywords TEXT, -- JSON array
  target_urls TEXT, -- JSON array
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### `entities` - Extraherade entiteter från målsidor
```sql
CREATE TABLE entities (
  id INTEGER PRIMARY KEY,
  customer_id INTEGER NOT NULL,
  target_url TEXT NOT NULL,
  entity_text TEXT NOT NULL,
  entity_type TEXT, -- PERSON, ORG, PRODUCT, LOCATION, etc.
  relevance_score REAL,
  extracted_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### `planning_metrics` - Metrics för utvärdering
```sql
CREATE TABLE planning_metrics (
  id INTEGER PRIMARY KEY,
  plan_id INTEGER NOT NULL REFERENCES link_plans(id),
  metric_name TEXT,
  metric_value REAL,
  calculated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

---

## Implementation Plan - Fas 1-3

### **FAS 1: Foundation (V1.0)** - Vecka 1-2

**Mål:** Grundläggande infrastruktur och datahantering

**Tasks:**
1. ✅ Skapa projektstruktur
2. ✅ Designa databas schema
3. ⬜ Implementera Planning Document Manager
   - Läsa från Google Sheets
   - Identifiera customer_id och länkar
4. ⬜ Implementera Link History Analyzer (basic)
   - Räkna länkar per kund
   - Hitta vanligaste ankartexter
5. ⬜ Implementera Customer Grouper
   - Gruppera baserat på antal länkar
6. ⬜ Skapa databas migrations
7. ⬜ Testa med verklig data

**Deliverables:**
- Fungerande dataimport från Sheets
- Grundläggande analys av historik
- Kunder grupperade per strategi

---

### **FAS 2: Semantic Core (V2.0)** - Vecka 3-4

**Mål:** Semantisk analys och intelligent planering

**Tasks:**
1. ⬜ Entity Extractor
   - Scrapa målsidor
   - Extrahera nyckelord och entiteter
   - NLP-analys av innehåll
2. ⬜ Phrase Finder
   - Hitta semantiskt relaterade fraser
   - Använd word embeddings
3. ⬜ Topic Clusterer
   - Gruppera sidor i topics
   - LDA/NMF topic modeling
4. ⬜ Anchor Text Optimizer
   - Generera diversifierade ankartexter
   - Följa naturlig distribution

**Deliverables:**
- Semantisk analys fungerar
- Topic clusters identifieras
- Ankartexter genereras automatiskt

---

### **FAS 3: Automation & Intelligence (V3.0)** - Vecka 5-6

**Mål:** Fullständig automatisering och smart planering

**Tasks:**
1. ⬜ Authority Builder
   - Planera länkar för topical authority
   - Internal linking strategy
2. ⬜ Planning Generator (komplett)
   - Kombinera alla moduler
   - Generera färdiga planer
3. ⬜ Export till Google Sheets
   - Skriv tillbaka till planeringsdokument
   - Formatera snyggt
4. ⬜ Web UI (optional)
   - Dashboard för att se planer
   - Redigera och godkänna planer
5. ⬜ Metrics & Evaluation
   - Mät kvalitet på planer
   - A/B test olika strategier

**Deliverables:**
- Fullständigt automatiserad planering
- Export till Sheets fungerar
- System redo för produktion

---

## Technology Stack

### Core
- **Python 3.8+**
- **SQLite** - Databas
- **Pandas** - Dataanalys

### NLP & Semantic
- **spaCy** - NLP och entity extraction
- **Gensim** - Topic modeling (LDA)
- **scikit-learn** - Clustering, TF-IDF
- **sentence-transformers** - Semantic similarity

### Web Scraping
- **BeautifulSoup4** - HTML parsing
- **requests** - HTTP requests
- **scrapy** (optional) - Advanced scraping

### Google Sheets
- **gspread** - Google Sheets API
- **google-auth** - Authentication

### Visualization (optional)
- **matplotlib/seaborn** - Charts
- **plotly** - Interactive plots

### Web UI (optional, Fas 3)
- **Flask/FastAPI** - Backend
- **React/Vue** - Frontend

---

## Exempel på användning (Efter Fas 3)

```python
from app.planning import LinkPlanner

# 1. Skapa planner
planner = LinkPlanner(
    planning_sheet_url="https://docs.google.com/spreadsheets/d/...",
    strategy="semantic_authority"
)

# 2. Analysera och planera
plan = planner.create_plan()

# 3. Granska plan
print(f"Skapade plan för {len(plan.customers)} kunder")
print(f"Totalt {plan.total_links} länkar planerade")

# 4. Se semantic clusters
for cluster in plan.get_clusters():
    print(f"\nCluster: {cluster.name}")
    print(f"  Topic: {cluster.topic}")
    print(f"  Keywords: {', '.join(cluster.keywords)}")
    print(f"  URLs: {len(cluster.urls)}")

# 5. Exportera
planner.export_to_sheets()  # Tillbaka till Google Sheets
planner.export_to_csv("link_plan.csv")  # Till CSV
planner.save_to_database()  # Till databas

# 6. Visa metrics
metrics = planner.get_metrics()
print(f"Semantic diversity: {metrics.semantic_diversity}")
print(f"Anchor distribution: {metrics.anchor_distribution}")
print(f"Topic coverage: {metrics.topic_coverage}")
```

---

## Success Metrics

### Kvalitet
- **Semantic diversity** - Hur varierade är ankartexter semantiskt?
- **Natural distribution** - Följer ankartexter naturlig fördelning?
- **Topic coverage** - Täcker länkar olika topics?
- **Authority score** - Potential för topical authority

### Effektivitet
- **Time saved** - Hur mycket tid sparas vs manuell planering?
- **Links per hour** - Hur många länkar kan planeras per timme?
- **Automation rate** - % av planer som inte behöver manuell justering

### Business
- **Customer satisfaction** - Nöjdhet med planer
- **SEO performance** - Faktiska SEO-resultat (långsiktigt)
- **Scalability** - Hur många kunder kan hanteras?

---

## Risks & Mitigation

| Risk | Sannolikhet | Impact | Mitigation |
|------|-------------|--------|------------|
| NLP fungerar dåligt på svenska | Medel | Hög | Använd flerspråkiga modeller, träna egen |
| Google Sheets API rate limits | Låg | Medel | Caching, batch operations |
| Målsidor svåra att scrapa | Hög | Medel | Fallback till manuell input |
| Semantic clustering inte meningsfullt | Medel | Hög | Human-in-the-loop review |
| För komplex för användare | Låg | Medel | Stegvis lansering, bra UI |

---

## Next Steps

1. **Godkänn plan** - Review och godkänn denna plan
2. **Setup miljö** - Installera dependencies
3. **Skapa databas** - Kör migrations
4. **Börja Fas 1** - Implementera foundation
5. **Iterera** - Testa och förbättra kontinuerligt

---

## Frågor att besvara

- [ ] Hur får vi tillgång till Google Sheets API?
- [ ] Vilka målsidor är tillgängliga för scraping?
- [ ] Finns det existerande SEO-data vi kan använda?
- [ ] Vilka språk ska systemet stödja? (Svenska, Engelska, annat?)
- [ ] Ska användare kunna redigera automatiska planer?
- [ ] Vad är acceptabel processtid? (sekunder, minuter?)

---

**Version:** 1.0
**Skapad:** 2025-11-05
**Senast uppdaterad:** 2025-11-05
**Status:** Planning - Awaiting approval

