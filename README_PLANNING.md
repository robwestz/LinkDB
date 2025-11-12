# Intelligent Link Planning System - README

## 🎯 Overview

Ett intelligente system för automatisk länkplanering baserat på:
- **Semantisk SEO** - Semantiskt relaterade sökfraser och entiteter
- **Topical Authority** - Bygga auktoritet genom strategiska länkkluster
- **Historisk data** - Lära från vad som fungerat tidigare
- **Automatisering** - Från analys till färdig plan på minuter istället för dagar

## 📁 Projektstruktur

```
linkdb/
├── app/
│   ├── analyzers/          # Analysera historisk länkdata
│   │   ├── link_history_analyzer.py
│   │   └── __init__.py
│   │
│   ├── planning/           # Kärnplanering
│   │   ├── customer_grouper.py
│   │   ├── db_manager.py
│   │   ├── plan_generator.py  (kommer i Fas 1)
│   │   └── __init__.py
│   │
│   ├── semantic/           # NLP & semantisk analys
│   │   ├── entity_extractor.py  (kommer i Fas 2)
│   │   ├── phrase_finder.py     (kommer i Fas 2)
│   │   ├── topic_clusterer.py   (kommer i Fas 2)
│   │   └── __init__.py
│   │
│   ├── integration/        # Externa integrationer
│   │   ├── sheets_manager.py    (kommer i Fas 1)
│   │   └── __init__.py
│   │
│   ├── schema_planning.sql  # Databas schema
│   └── settings.py
│
├── data/
│   ├── input/
│   │   └── main_sheet.xlsx
│   └── output/
│       ├── linkops_history.db
│       └── linkops_planning.db  (nytt)
│
├── init_planning_system.py        # Initialisering & demo
├── PLANNING_SYSTEM_SPEC.md        # Fullständig specifikation
├── requirements_planning.txt      # Dependencies
└── README_PLANNING.md             # Denna fil
```

## 🚀 Snabbstart

### 1. Installation

```bash
# Aktivera virtuell miljö
.venv\Scripts\activate

# Installera dependencies
pip install -r requirements_planning.txt

# Ladda ner spaCy-modeller för NLP
python -m spacy download sv_core_news_sm  # Svenska
python -m spacy download en_core_web_sm   # Engelska
```

### 2. Initiera systemet

```bash
python init_planning_system.py
```

Detta skapar:
- Planning database (`linkops_planning.db`)
- Default strategier
- Demonstrerar grundfunktionalitet

### 3. Testa modulerna

```bash
# Testa Customer Grouper
python app/planning/customer_grouper.py

# Testa Link History Analyzer
python app/analyzers/link_history_analyzer.py
```

## 📊 Databas Schema

### Huvudtabeller

#### `link_plans`
Färdiga länkplaner.

**Kolumner:**
- `id` - Plan ID
- `plan_name` - Namn på planen
- `status` - draft, approved, in_progress, completed
- `total_links` - Totalt antal länkar i planen
- `semantic_strategy` - Vilken strategi användes
- `created_at` - När planen skapades

#### `planned_links`
Individuella länkar i planen.

**Kolumner:**
- `id` - Länk ID
- `plan_id` - Referens till link_plans
- `customer_id` - Kund
- `target_url` - Målsida
- `anchor_text` - Ankartext
- `anchor_type` - exact, partial, branded, generic, lsi
- `semantic_cluster_id` - Vilket semantiskt kluster
- `topic` - Ämne/topic
- `priority_score` - Prioritet (0-1)
- `reasoning` - Förklaring av valet
- `status` - planned, published, cancelled

#### `semantic_clusters`
Semantiska grupperingar av målsidor.

**Kolumner:**
- `id` - Cluster ID
- `customer_id` - Kund
- `cluster_name` - Namn på klustret
- `topic` - Huvudämne
- `keywords` - Nyckelord (JSON array)
- `target_urls` - URLs i klustret (JSON array)

#### `entities`
Extraherade entiteter från målsidor.

**Kolumner:**
- `target_url` - Målsida
- `entity_text` - Entitetstexten
- `entity_type` - PERSON, ORG, PRODUCT, LOCATION, etc.
- `relevance_score` - Hur relevant (0-1)

## 🎨 Strategier

Systemet använder olika strategier baserat på antal tillgängliga länkar:

### Single Focus (1 länk)
- **Fokus:** En starkt optimerad länk
- **Ankartexter:** 50% exact, 50% branded
- **Semantic clustering:** Nej
- **Authority building:** Nej

### Diversified Basics (2-5 länkar)
- **Fokus:** Diversifiera ankartexter
- **Ankartexter:** 20% exact, 30% partial, 30% branded, 20% generic
- **Semantic clustering:** Nej
- **Authority building:** Nej

### Semantic Foundation (6-15 länkar)
- **Fokus:** Börja bygga semantiska kluster
- **Ankartexter:** 15% exact, 35% partial, 20% branded, 20% generic, 10% LSI
- **Semantic clustering:** Ja
- **Authority building:** Ja (grundläggande)

### Topical Authority (16-30 länkar)
- **Fokus:** Full topical authority-strategi
- **Ankartexter:** 10% exact, 35% partial, 20% branded, 20% generic, 15% LSI
- **Semantic clustering:** Ja
- **Authority building:** Ja (avancerad)

### Enterprise Authority (31+ länkar)
- **Fokus:** Enterprise-strategi med djup topic coverage
- **Ankartexter:** 8% exact, 37% partial, 20% branded, 20% generic, 15% LSI
- **Semantic clustering:** Ja
- **Authority building:** Ja (komplett)

## 🔍 Moduler

### Customer Grouper
Grupperar kunder baserat på antal tillgängliga länkar.

```python
from app.planning.customer_grouper import CustomerGrouper

grouper = CustomerGrouper("path/to/linkops_history.db")

# Simulera counts från planeringsdokument
customer_counts = {
    117: 15,  # bethard.com med 15 länkar
    118: 5,   # annan kund med 5 länkar
}

groups = grouper.group_customers(customer_counts)
grouper.print_summary(groups)
```

### Link History Analyzer
Analyserar historisk länkdata för en kund.

```python
from app.analyzers.link_history_analyzer import LinkHistoryAnalyzer

analyzer = LinkHistoryAnalyzer("path/to/linkops_history.db")
analysis = analyzer.analyze_customer(117)

if analysis:
    analyzer.print_analysis(analysis)
```

**Output inkluderar:**
- Totalt antal länkar
- Anchor diversity score
- Vanligaste ankartexter
- Mest länkade URLs
- Primär strategi som används
- Rekommendationer

## 📝 Användningsexempel

### Scenario 1: Analysera en kund

```python
from app.analyzers.link_history_analyzer import LinkHistoryAnalyzer

# Skapa analyzer
analyzer = LinkHistoryAnalyzer("data/output/linkops_history.db")

# Analysera customer_id 117
analysis = analyzer.analyze_customer(117)

# Se resultatet
print(f"Kund: {analysis.canonical_root}")
print(f"Totalt länkar: {analysis.total_links}")
print(f"Anchor diversity: {analysis.anchor_diversity_score:.2f}")
print(f"Strategi: {analysis.primary_strategy}")

for rec in analysis.recommendations:
    print(f"  • {rec}")
```

### Scenario 2: Gruppera kunder från planeringsdokument

```python
from app.planning.customer_grouper import CustomerGrouper

# Counts från Google Sheets (kommer i Fas 1)
planning_counts = {
    101: 8,
    102: 15,
    103: 3,
    104: 25,
}

grouper = CustomerGrouper("data/output/linkops_history.db")
groups = grouper.group_customers(planning_counts)

# Se vilka strategier som rekommenderas
for group in groups:
    print(f"{group.canonical_root}: {group.recommended_strategy}")
    print(f"  Can cluster: {group.can_semantic_cluster}")
    print(f"  Can build authority: {group.can_build_authority}")
```

## 🔮 Roadmap

### ✅ Fas 1: Foundation (v1.0) - PÅGÅR
- [x] Databas schema
- [x] Customer Grouper
- [x] Link History Analyzer
- [ ] Google Sheets integration
- [ ] Enkel plan generator

**ETA:** Vecka 1-2

### 🔄 Fas 2: Semantic Core (v2.0)
- [ ] Entity Extractor
- [ ] Phrase Finder
- [ ] Topic Clusterer
- [ ] Anchor Text Optimizer

**ETA:** Vecka 3-4

### 🔮 Fas 3: Automation & Intelligence (v3.0)
- [ ] Authority Builder
- [ ] Fullständig Planning Generator
- [ ] Export till Google Sheets
- [ ] Web UI (optional)
- [ ] Metrics & Evaluation

**ETA:** Vecka 5-6

## 📚 Dependencies

**Core:**
- Python 3.8+
- SQLite
- rich (output formatting)

**NLP & Semantic (Fas 2):**
- spaCy (entity extraction)
- gensim (topic modeling)
- scikit-learn (clustering)
- sentence-transformers (semantic similarity)

**Integration:**
- gspread (Google Sheets API)
- google-auth

**Web Scraping:**
- BeautifulSoup4
- requests

## 🐛 Troubleshooting

### Problem: "Database not found"
**Lösning:** Kör `python init_planning_system.py` för att skapa databasen.

### Problem: "No module named 'spacy'"
**Lösning:** 
```bash
pip install spacy
python -m spacy download sv_core_news_sm
```

### Problem: Google Sheets API credentials
**Lösning:** Kommer i Fas 1 - vi skapar en guide för att sätta upp credentials.

## 📖 Dokumentation

- **PLANNING_SYSTEM_SPEC.md** - Fullständig systemspecifikation
- **README_PLANNING.md** - Denna fil
- Kod-kommentarer i varje modul

## 🤝 Bidra

För att lägga till ny funktionalitet:

1. Läs `PLANNING_SYSTEM_SPEC.md` för arkitektur
2. Skapa nya moduler i relevant mapp
3. Följ befintlig kodstil
4. Lägg till docstrings
5. Testa din kod

## 📞 Support

Se `PLANNING_SYSTEM_SPEC.md` för:
- Detaljerad arkitektur
- Dataflöden
- Implementation plan
- FAQ

## ✅ Status

**Current Version:** 1.0-alpha (Fas 1 påbörjad)

**Completed:**
- ✅ Databas schema
- ✅ Customer Grouper
- ✅ Link History Analyzer
- ✅ Planning DB Manager

**In Progress:**
- 🔄 Google Sheets integration
- 🔄 Plan Generator (basic)

**Coming Soon:**
- ⏳ Semantic SEO Engine
- ⏳ Full automation

---

**🎯 Mål:** Automatisera länkplanering från dagar till minuter!

**💡 Vision:** Ett system som är smartare än en mänsklig planerare genom att kombinera historisk data, semantisk analys och AI.

