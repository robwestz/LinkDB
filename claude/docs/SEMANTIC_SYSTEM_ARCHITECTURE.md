# Semantic SEO System - Technical Architecture & Implementation Plan

**Vision:** Reverse-engineer Google's search intent through semantic analysis of link context, SERP patterns, and entity clustering to generate data-driven link building strategies.

---

## 🎯 System Overview

### The Three-Pillar Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SEMANTIC SEO SYSTEM                       │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐  │
│  │   PILLAR 1   │  │   PILLAR 2   │  │    PILLAR 3     │  │
│  │              │  │              │  │                 │  │
│  │   Context    │  │    SERP      │  │   Strategy      │  │
│  │  Extraction  │  │   Analysis   │  │   Generation    │  │
│  │              │  │              │  │                 │  │
│  │  • Scrape    │  │  • Entity    │  │  • Combine      │  │
│  │  • Parse     │  │    search    │  │    all data     │  │
│  │  • Extract   │  │  • Cluster   │  │  • LLM synth    │  │
│  │  • Classify  │  │    search    │  │  • Generate     │  │
│  │              │  │  • Intent    │  │    specs        │  │
│  └──────┬───────┘  └──────┬───────┘  └────────┬────────┘  │
│         │                  │                   │           │
│         └──────────────────┴───────────────────┘           │
│                            │                               │
│                  ┌─────────▼──────────┐                    │
│                  │   RECOMMENDATION   │                    │
│                  │      ENGINE        │                    │
│                  └────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🏗️ Pillar 1: Context Extraction & Analysis

### Objective
Extract and understand the textual context surrounding every backlink to determine semantic relevance and topical alignment.

### Components

#### 1.1 Context Scraper
**Purpose:** Fetch and parse the publishing page to extract link context.

**Input:**
- `pub_page_url` from `links_history` table

**Process:**
1. **HTTP Request** with rotation headers to avoid detection
   ```python
   headers = {
       'User-Agent': random.choice(USER_AGENTS),
       'Accept': 'text/html',
       'Accept-Language': 'en-US,en;q=0.9,sv;q=0.8'
   }
   response = requests.get(url, headers=headers, timeout=30)
   ```

2. **HTML Parsing** with BeautifulSoup4
   ```python
   soup = BeautifulSoup(response.content, 'html.parser')
   ```

3. **Link Locator** - Find the specific `<a>` tag
   ```python
   # Match by href (target_url) and anchor text
   link_element = soup.find('a', href=target_url, string=anchor_text)
   ```

4. **Context Extraction** - Get surrounding content
   ```python
   # Get parent paragraph or div
   parent = link_element.find_parent(['p', 'div', 'li', 'td'])

   # Extract ±200 words around the link
   full_text = parent.get_text()
   # ... logic to extract window around link position
   ```

5. **Metadata Extraction**
   ```python
   metadata = {
       'title': soup.find('title').get_text(),
       'meta_description': soup.find('meta', {'name': 'description'})['content'],
       'h1': soup.find('h1').get_text() if soup.find('h1') else None,
       'h2_above_link': find_heading_above(link_element, 'h2'),
       'h3_above_link': find_heading_above(link_element, 'h3'),
       'image_alt': link_element.find('img')['alt'] if link_element.find('img') else None
   }
   ```

**Output:**
- Store in `links_history.context_excerpt`
- Store metadata in new table `link_context_metadata`

**Schema Extension:**
```sql
CREATE TABLE link_context_metadata (
    id INTEGER PRIMARY KEY,
    link_id INTEGER NOT NULL,
    page_title TEXT,
    meta_description TEXT,
    h1_text TEXT,
    h2_above_link TEXT,
    h3_above_link TEXT,
    paragraph_text TEXT,  -- Full paragraph containing link
    context_window TEXT,  -- ±200 words
    scraped_at DATETIME,
    scrape_success BOOLEAN,
    scrape_error TEXT,
    FOREIGN KEY (link_id) REFERENCES links_history(id)
);
```

**Error Handling:**
- 404/403/500: Mark as `scrape_success = FALSE`, log error
- Timeout: Retry 3 times with exponential backoff
- Blocked: Use proxy rotation or headless browser (Playwright)

**Rate Limiting:**
- Max 10-15 requests/minute to avoid IP bans
- Randomize delay between requests (2-5 seconds)
- Respect robots.txt (optional, configurable)

**Estimated Time:**
- 4,736 links ÷ 12 requests/min = ~6.5 hours
- Can run overnight or over weekend

**Cost:**
- Free (just scraping)
- Optional: Proxy service (~$10/month for 10k requests)

---

#### 1.2 LLM Entity & Topic Extractor
**Purpose:** Use LLM to understand *what* the context is about.

**Input:**
- `context_excerpt` or `context_window`
- `page_title`, `h2_above_link`

**LLM Prompt Template:**
```
You are an SEO expert analyzing backlink context.

Given the following information about a link:
- Page title: "{page_title}"
- Section heading: "{h2_above_link}"
- Link anchor: "{anchor_text}"
- Link context (surrounding text): "{context_window}"
- Target URL: "{target_url}"

Extract the following information as JSON:

1. **Named Entities:**
   - Brands mentioned
   - Products mentioned
   - Locations mentioned
   - People mentioned

2. **Topic Classification:**
   - Primary topic (1-3 words)
   - Secondary topics (comma-separated)
   - Industry category

3. **Search Intent:**
   - Intent type: informational, commercial, navigational, transactional
   - Confidence: 0-100

4. **Semantic Keywords:**
   - Main keywords (5-10)
   - LSI keywords (related terms, 5-10)
   - Long-tail phrases (2-3)

5. **Link Purpose:**
   - Citation (reference/source)
   - Recommendation (endorsement)
   - Example (case study)
   - Comparison (vs competitor)
   - Definition (explanation)

Output only valid JSON, no other text.
```

**Expected Output:**
```json
{
  "entities": {
    "brands": ["Bethard", "Unibet"],
    "products": ["live betting", "sportsbook"],
    "locations": ["Sweden", "Allsvenskan"],
    "people": []
  },
  "topics": {
    "primary": "sports betting",
    "secondary": "live odds, football betting, Swedish gambling",
    "category": "gambling"
  },
  "intent": {
    "type": "commercial",
    "confidence": 85
  },
  "keywords": {
    "main": ["betting", "odds", "live", "sport", "football"],
    "lsi": ["wagering", "gambling", "sportsbook", "bookmaker", "in-play"],
    "long_tail": ["live betting on Swedish football", "best odds for Allsvenskan"]
  },
  "link_purpose": "recommendation"
}
```

**Storage:**
```sql
CREATE TABLE semantic_entities (
    id INTEGER PRIMARY KEY,
    link_id INTEGER NOT NULL,
    entity_type TEXT,  -- brand, product, location, person
    entity_value TEXT,
    FOREIGN KEY (link_id) REFERENCES links_history(id)
);

CREATE TABLE semantic_topics (
    id INTEGER PRIMARY KEY,
    link_id INTEGER NOT NULL,
    primary_topic TEXT,
    secondary_topics TEXT,  -- comma-separated
    category TEXT,
    FOREIGN KEY (link_id) REFERENCES links_history(id)
);

CREATE TABLE semantic_intent (
    id INTEGER PRIMARY KEY,
    link_id INTEGER NOT NULL,
    intent_type TEXT,
    confidence INTEGER,
    link_purpose TEXT,
    FOREIGN KEY (link_id) REFERENCES links_history(id)
);

CREATE TABLE semantic_keywords (
    id INTEGER PRIMARY KEY,
    link_id INTEGER NOT NULL,
    keyword TEXT,
    keyword_type TEXT,  -- main, lsi, long_tail
    FOREIGN KEY (link_id) REFERENCES links_history(id)
);
```

**LLM Selection:**
- **GPT-4 Turbo:** Best accuracy, ~$0.005/link
- **Claude 3.5 Sonnet:** Fast, good accuracy, ~$0.004/link
- **Gemini 1.5 Pro:** Free tier available, ~$0.003/link
- **GPT-3.5 Turbo:** Cheapest, decent accuracy, ~$0.001/link

**Recommendation:** Start with GPT-3.5 Turbo for speed/cost, upgrade to GPT-4 for critical analysis.

**Batch Processing:**
- Process 100 links at a time
- Parallel requests (5-10 concurrent)
- Total time: ~30-60 minutes for all 4,736 links

**Cost Estimate:**
- 4,736 links × $0.005 = **$23.68** (one-time)
- New links: ~$0.005/link ongoing

---

#### 1.3 Semantic Clustering
**Purpose:** Group links by semantic similarity to identify topical clusters.

**Approach:**
1. **Vectorize Keywords**
   - Use embedding model (e.g., `text-embedding-ada-002` or open-source `sentence-transformers`)
   - Convert each link's keywords into a vector

   ```python
   from sentence_transformers import SentenceTransformer

   model = SentenceTransformer('all-MiniLM-L6-v2')

   # For each link
   keywords = link['main_keywords'] + link['lsi_keywords']
   embedding = model.encode(' '.join(keywords))
   ```

2. **Clustering Algorithm**
   - Use K-Means, DBSCAN, or Hierarchical Clustering
   - Determine optimal number of clusters (elbow method)

   ```python
   from sklearn.cluster import DBSCAN

   clustering = DBSCAN(eps=0.3, min_samples=5).fit(embeddings)
   cluster_labels = clustering.labels_
   ```

3. **Cluster Naming**
   - Use LLM to generate descriptive cluster names
   ```
   Given these keywords from a cluster:
   ["betting", "odds", "live", "sport", "football", "wagering", ...]

   Generate a concise 2-4 word name for this semantic cluster.
   ```

**Storage:**
```sql
CREATE TABLE semantic_clusters (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    cluster_name TEXT,
    cluster_keywords TEXT,  -- JSON array
    cluster_size INTEGER,   -- number of links
    created_at DATETIME,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE link_clusters (
    id INTEGER PRIMARY KEY,
    link_id INTEGER NOT NULL,
    cluster_id INTEGER NOT NULL,
    FOREIGN KEY (link_id) REFERENCES links_history(id),
    FOREIGN KEY (cluster_id) REFERENCES semantic_clusters(id)
);
```

**Use Case:**
- Identify which topics are over-represented or under-represented
- Find gaps in topical coverage
- Suggest new link topics for better topic authority

---

## 🔍 Pillar 2: SERP Reverse Engineering

### Objective
Understand what Google *wants* to see for a given keyword/entity by analyzing SERP results.

### Components

#### 2.1 Three-Search Strategy

**Search 1: Entity Search**
- Query: The brand/product name itself
- Example: "Bethard"
- Purpose: Understand how Google perceives the entity

**Search 2: Broad Cluster Search**
- Query: Category or broad topic
- Example: "betting sites Sweden"
- Purpose: Identify category-level intent signals

**Search 3: Specific Cluster Search**
- Query: Niche/specific topic
- Example: "live football betting odds"
- Purpose: Identify specific intent signals

**For each search:**
1. **Fetch SERP**
   - Use Google Custom Search API (100 free queries/day, then $5/1000)
   - Or scrape with headless browser (Playwright/Selenium)

2. **Extract SERP Features**
   ```python
   serp_data = {
       'query': search_query,
       'results': [
           {
               'rank': 1,
               'title': "...",
               'url': "...",
               'description': "...",
               'domain': "...",
               'type': "organic"  # or featured_snippet, people_also_ask, etc
           },
           # ... top 10
       ],
       'featured_snippet': { ... },
       'people_also_ask': [ ... ],
       'related_searches': [ ... ]
   }
   ```

3. **Store Results**
   ```sql
   CREATE TABLE serp_searches (
       id INTEGER PRIMARY KEY,
       customer_id INTEGER,
       target_url TEXT,
       search_query TEXT,
       search_type TEXT,  -- entity, broad_cluster, specific_cluster
       searched_at DATETIME,
       FOREIGN KEY (customer_id) REFERENCES customers(id)
   );

   CREATE TABLE serp_results (
       id INTEGER PRIMARY KEY,
       search_id INTEGER NOT NULL,
       rank INTEGER,
       title TEXT,
       url TEXT,
       description TEXT,
       domain TEXT,
       result_type TEXT,
       FOREIGN KEY (search_id) REFERENCES serp_searches(id)
   );
   ```

#### 2.2 SERP Analysis with LLM

**Purpose:** Synthesize insights from all 3 searches.

**LLM Prompt:**
```
You are a Google algorithm reverse-engineering expert.

I performed 3 Google searches related to "{brand}" ({target_url}):

1. Entity search: "{entity_query}"
   Top 3 results:
   - Title: "...", Description: "..."
   - Title: "...", Description: "..."
   - Title: "...", Description: "..."

2. Broad cluster search: "{broad_query}"
   Top 3 results:
   - Title: "...", Description: "..."
   - ...

3. Specific cluster search: "{specific_query}"
   Top 3 results:
   - Title: "...", Description: "..."
   - ...

Analyze these SERPs and provide:

1. **Dominant Search Intent:**
   - What type of intent does Google prioritize? (informational, commercial, navigational, transactional)
   - Confidence: 0-100

2. **Key Semantic Signals:**
   - What words/phrases appear most frequently in titles and descriptions?
   - What topics does Google associate with this entity?

3. **Content Structure Patterns:**
   - What content format does Google prefer? (list, guide, comparison, review, etc)
   - What structure do top results use?

4. **Optimal Link Strategy:**
   - What anchor text style would align with this intent?
   - What context/topic should the publishing page cover?
   - Recommended anchor distribution: exact, partial, branded, generic, LSI

Output as JSON.
```

**Expected Output:**
```json
{
  "dominant_intent": {
    "type": "commercial_with_informational",
    "confidence": 85,
    "reasoning": "Top results mix comparisons (commercial) with guides (informational)"
  },
  "semantic_signals": [
    {
      "signal": "bonus",
      "frequency": 7,
      "importance": "high"
    },
    {
      "signal": "license",
      "frequency": 5,
      "importance": "medium"
    },
    {
      "signal": "odds",
      "frequency": 8,
      "importance": "high"
    }
  ],
  "content_patterns": {
    "preferred_format": "comparison_table_with_review",
    "structure": ["intro", "comparison table", "detailed reviews", "FAQ"],
    "avg_word_count": 2500
  },
  "link_strategy": {
    "recommended_context_topic": "Comparison of Swedish betting sites with focus on live odds",
    "optimal_anchor_distribution": {
      "exact_match": 10,
      "partial_match": 40,
      "branded": 25,
      "generic": 15,
      "lsi": 10
    },
    "anchor_examples": [
      {
        "type": "partial",
        "text": "live betting platforms in Sweden",
        "justification": "Aligns with commercial intent + geographic relevance"
      },
      {
        "type": "branded",
        "text": "Bethard",
        "justification": "Natural brand mention in comparison context"
      }
    ]
  }
}
```

**Storage:**
```sql
CREATE TABLE serp_analysis (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    target_url TEXT,
    analyzed_at DATETIME,
    dominant_intent TEXT,
    intent_confidence INTEGER,
    semantic_signals JSON,  -- JSON array of signals
    content_patterns JSON,
    optimal_strategy JSON,
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

**Cost:**
- SERP fetching: $5/1000 queries (Google API) or free (scraping)
- LLM analysis: ~$0.02 per 3-search analysis (GPT-4)
- Total for 10 target URLs: ~$0.20 one-time

---

## 🧠 Pillar 3: Strategy Generation

### Objective
Combine historical data + context analysis + SERP insights to generate optimal link building specifications.

### Components

#### 3.1 Data Synthesis

**Inputs:**
1. **Historical Performance** (from analyzers)
   - What anchors worked well historically?
   - What link velocity is sustainable?
   - What domain types performed best?

2. **Context Analysis** (from Pillar 1)
   - What topics are currently covered?
   - What semantic gaps exist?
   - What entity associations are strong?

3. **SERP Intelligence** (from Pillar 2)
   - What does Google want to see?
   - What intent signals matter?
   - What content structure works?

**Synthesis Process:**
```python
def synthesize_strategy(customer_id, target_url):
    # Fetch historical data
    history = get_historical_performance(customer_id)

    # Fetch semantic analysis
    context = get_semantic_analysis(customer_id)

    # Fetch SERP analysis
    serp = get_serp_analysis(target_url)

    # Combine
    synthesis = {
        'historical_strength': history.primary_strategy,
        'current_topic_coverage': context.cluster_distribution,
        'google_intent': serp.dominant_intent,
        'gaps': identify_gaps(history, context, serp)
    }

    return synthesis
```

#### 3.2 LLM Strategy Generator

**Master Prompt:**
```
You are an expert SEO strategist specializing in link building.

Your task: Generate a comprehensive, data-driven link building strategy.

**Customer:** {brand} ({canonical_root})
**Target URL:** {target_url}

**Historical Performance:**
- Total links: {total_links}
- Current strategy: {primary_strategy}
- Anchor quality score: {anchor_quality}
- Over-optimization risk: {over_opt_risk}
- Successful anchors: {top_anchors}
- Successful domains: {top_domains}

**Current Topic Coverage:**
- Primary topics: {primary_topics}
- Semantic clusters: {clusters}
- Entity associations: {entities}
- Coverage gaps: {gaps}

**Google SERP Intelligence:**
- Dominant intent: {dominant_intent}
- Key signals Google prioritizes: {semantic_signals}
- Preferred content format: {content_format}
- Optimal anchor distribution: {optimal_distribution}

**Task:**
Generate 10 specific link building recommendations. For each recommendation, provide:

1. **Link Specification:**
   - Anchor text (exact wording)
   - Anchor type (exact, partial, branded, generic, LSI)
   - Link purpose (citation, recommendation, example, comparison)

2. **Publishing Page Specification:**
   - Article topic (1 sentence)
   - Section heading where link should appear
   - Context paragraph (±50 words showing how link naturally fits)
   - Content format (guide, list, comparison, review, news, etc)

3. **Target Domain Characteristics:**
   - Domain type (news, blog, directory, niche site, etc)
   - Geographic relevance (Sweden, international, etc)
   - Authority level (prefer high/medium/low DA)

4. **Reasoning:**
   - Why this anchor/context combination?
   - How does it align with Google's intent?
   - How does it fill current gaps?
   - Risk level (low, medium, high)

Output as JSON array of 10 recommendations.
```

**Expected Output:**
```json
{
  "recommendations": [
    {
      "priority": 1,
      "link_spec": {
        "anchor_text": "live odds på Allsvenskan",
        "anchor_type": "partial_match",
        "link_purpose": "recommendation"
      },
      "publishing_spec": {
        "article_topic": "Guide: Best platforms for betting on Swedish football",
        "section_heading": "Where to find the best live odds",
        "context_paragraph": "För svenska fotbollsfans som vill satsa på Allsvenskan är det viktigt att hitta plattformar med konkurrenskraftiga [live odds på Allsvenskan]. Bra plattformar uppdaterar sina odds i realtid och erbjuder cash-out funktioner under matcherna.",
        "content_format": "guide",
        "estimated_word_count": 1500
      },
      "domain_spec": {
        "domain_type": "sports_news_site",
        "geographic": "Sweden",
        "authority_preference": "medium_to_high",
        "tld_preference": ".se"
      },
      "reasoning": {
        "intent_alignment": "Aligns with Google's commercial + informational intent mix",
        "gap_filling": "Currently only 5% of anchors mention 'Allsvenskan' - Swedish relevance gap",
        "natural_fit": "Partial match anchor in educational context = low over-optimization risk",
        "serp_signal_match": "Matches Google's emphasis on 'odds' and geographic relevance",
        "risk_level": "low"
      },
      "metadata": {
        "estimated_difficulty": "medium",
        "priority_score": 95
      }
    },
    {
      "priority": 2,
      "link_spec": {
        "anchor_text": "Bethard",
        "anchor_type": "branded",
        "link_purpose": "comparison"
      },
      "publishing_spec": {
        "article_topic": "Comparison: Sweden's top betting sites 2025",
        "section_heading": "Live betting comparison table",
        "context_paragraph": "I vår jämförelse av live betting-plattformar rankar [Bethard] högt tack vare sina snabba odduppdateringar och användarvänliga interface. Plattformen är licensierad i Sverige och erbjuder konkurrenskraftiga odds på både fotboll och andra sporter.",
        "content_format": "comparison_table",
        "estimated_word_count": 2000
      },
      "domain_spec": {
        "domain_type": "gambling_review_site",
        "geographic": "Sweden",
        "authority_preference": "high",
        "tld_preference": ".se or .com"
      },
      "reasoning": {
        "intent_alignment": "Perfect for commercial intent SERPs",
        "gap_filling": "Only 3.6% branded anchors currently - need more for naturality",
        "natural_fit": "Branded mention in comparison context is highly natural",
        "serp_signal_match": "Comparison format matches Google's preferred content structure",
        "risk_level": "very_low"
      },
      "metadata": {
        "estimated_difficulty": "high",
        "priority_score": 92
      }
    }
    // ... 8 more recommendations
  ],
  "strategy_summary": {
    "total_recommendations": 10,
    "anchor_distribution": {
      "exact_match": 1,
      "partial_match": 4,
      "branded": 3,
      "generic": 1,
      "lsi": 1
    },
    "estimated_timeline": "2-3 months",
    "expected_impact": "+15-25% increase in ranking for target keywords",
    "risk_assessment": "Low - Strategy prioritizes naturality and diversity"
  }
}
```

**Storage:**
```sql
CREATE TABLE link_recommendations (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    target_url TEXT,
    priority INTEGER,
    anchor_text TEXT,
    anchor_type TEXT,
    article_topic TEXT,
    section_heading TEXT,
    context_paragraph TEXT,
    content_format TEXT,
    domain_type TEXT,
    geographic TEXT,
    reasoning JSON,
    priority_score INTEGER,
    created_at DATETIME,
    status TEXT DEFAULT 'pending',  -- pending, in_progress, completed
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);
```

**Cost:**
- LLM generation: ~$0.015 per 10-recommendation strategy
- Total for 10 customers: ~$0.15

---

## 🔄 Complete Workflow

### End-to-End Process

```
1. INPUT: Customer ID + Target URL
           ↓
2. PILLAR 1: Context Extraction
   ├─ Scrape publishing pages → context_excerpt
   ├─ LLM extract entities → semantic_entities
   ├─ LLM extract topics → semantic_topics
   └─ Cluster similar links → semantic_clusters
           ↓
3. PILLAR 2: SERP Analysis
   ├─ Search #1: Entity → serp_results
   ├─ Search #2: Broad cluster → serp_results
   ├─ Search #3: Specific cluster → serp_results
   └─ LLM analyze all → serp_analysis
           ↓
4. PILLAR 3: Strategy Synthesis
   ├─ Fetch historical data
   ├─ Fetch semantic data
   ├─ Fetch SERP data
   └─ LLM generate strategy → link_recommendations
           ↓
5. OUTPUT: 10 Link Specifications
   - Anchor text
   - Context paragraph
   - Article topic
   - Domain requirements
   - Reasoning
```

### Execution Script

```python
# semantic_pipeline.py

import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from semantic.context_scraper import ContextScraper
from semantic.entity_extractor import EntityExtractor
from semantic.serp_analyzer import SERPAnalyzer
from semantic.strategy_generator import StrategyGenerator

def run_semantic_pipeline(customer_id, target_url):
    """
    Run complete semantic analysis and strategy generation.
    """
    print(f"\n🚀 Running Semantic SEO Pipeline")
    print(f"Customer: {customer_id}")
    print(f"Target: {target_url}\n")

    # Step 1: Context Extraction
    print("📄 Step 1: Extracting link context...")
    scraper = ContextScraper(db_path)
    scraper.scrape_customer_links(customer_id)
    print("✅ Context extraction complete\n")

    # Step 2: Entity & Topic Extraction
    print("🧠 Step 2: Extracting entities and topics...")
    extractor = EntityExtractor(db_path, llm_provider='openai')
    extractor.extract_customer_semantics(customer_id)
    print("✅ Semantic extraction complete\n")

    # Step 3: SERP Analysis
    print("🔍 Step 3: Analyzing Google SERPs...")
    analyzer = SERPAnalyzer(db_path, llm_provider='openai')
    analyzer.analyze_target_url(customer_id, target_url)
    print("✅ SERP analysis complete\n")

    # Step 4: Strategy Generation
    print("🎯 Step 4: Generating link building strategy...")
    generator = StrategyGenerator(db_path, llm_provider='openai')
    strategy = generator.generate_strategy(customer_id, target_url, num_recommendations=10)
    print("✅ Strategy generation complete\n")

    # Print results
    print("="*70)
    print("GENERATED LINK RECOMMENDATIONS")
    print("="*70)
    for i, rec in enumerate(strategy['recommendations'], 1):
        print(f"\n{i}. Priority: {rec['priority']}")
        print(f"   Anchor: \"{rec['link_spec']['anchor_text']}\"")
        print(f"   Type: {rec['link_spec']['anchor_type']}")
        print(f"   Article: {rec['publishing_spec']['article_topic']}")
        print(f"   Risk: {rec['reasoning']['risk_level']}")

    print("\n✅ Pipeline complete!")

if __name__ == "__main__":
    customer_id = int(sys.argv[1]) if len(sys.argv) > 1 else 117
    target_url = sys.argv[2] if len(sys.argv) > 2 else "https://www.bethard.com/sv/sports"

    run_semantic_pipeline(customer_id, target_url)
```

---

## 💰 Cost Analysis

### One-Time Setup (All 4,736 links)

| Component | Unit Cost | Total |
|-----------|-----------|-------|
| Context scraping | Free | $0 |
| Entity extraction (GPT-3.5) | $0.001/link | $4.74 |
| Topic classification | Included above | $0 |
| Clustering | Free (local) | $0 |
| **Total One-Time** | | **$4.74** |

### Per-Strategy Generation (10 target URLs)

| Component | Unit Cost | Total |
|-----------|-----------|-------|
| SERP fetching (3 searches × 10 URLs) | Free (scraping) | $0 |
| SERP analysis (GPT-4) | $0.02/analysis | $0.20 |
| Strategy generation (GPT-4) | $0.015/strategy | $0.15 |
| **Total Per-Strategy Set** | | **$0.35** |

### Ongoing Costs (Per New Link)

| Component | Cost |
|-----------|------|
| Context scraping | $0 |
| Entity extraction | $0.001 |
| **Total Per New Link** | **$0.001** |

**Annual Estimate (assuming 1,000 new links/year):**
- New link processing: $1.00
- Quarterly strategy updates (4 × 10 URLs): $1.40
- **Total Annual:** ~$2.50

**Extremely affordable!**

---

## 📊 Success Metrics

### Technical Metrics
- [ ] Context extraction coverage: >95% of links
- [ ] Entity extraction accuracy: >90% (manual validation sample)
- [ ] SERP analysis completion: 100% of target URLs
- [ ] Strategy generation time: <5 min per customer

### Business Metrics
- [ ] Link effectiveness improvement: +30% vs manual
- [ ] Time saved per strategy: 2 hours → 5 minutes (96% reduction)
- [ ] Customer satisfaction: >4.5/5 rating on recommendations

### SEO Metrics
- [ ] Ranking improvement: +2-5 positions for target keywords (3-month test)
- [ ] Over-optimization reduction: -50% anchor risk flags
- [ ] Topical coverage improvement: +40% semantic cluster diversity

---

## 🚀 Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
- [ ] Week 1: Set up database schema extensions
- [ ] Week 2: Build context scraper (Pillar 1.1)
- [ ] Week 3: Build entity extractor (Pillar 1.2)
- [ ] Week 4: Test on 50 links, validate accuracy

**Deliverable:** All links have context + entities

### Phase 2: SERP Intelligence (Weeks 5-8)
- [ ] Week 5: Build SERP scraper/API integration
- [ ] Week 6: Build SERP analyzer (Pillar 2.2)
- [ ] Week 7: Analyze 10 target URLs
- [ ] Week 8: Validate SERP insights with SEO team

**Deliverable:** SERP analysis for top 10 URLs

### Phase 3: Strategy Engine (Weeks 9-12)
- [ ] Week 9: Build strategy generator (Pillar 3)
- [ ] Week 10: Generate 10 test strategies
- [ ] Week 11: Manual review + refinement
- [ ] Week 12: A/B test: AI vs manual strategies

**Deliverable:** Working strategy generator

### Phase 4: Production (Weeks 13-16)
- [ ] Week 13: Scale to all customers
- [ ] Week 14: GUI integration
- [ ] Week 15: Performance optimization
- [ ] Week 16: Team training + documentation

**Deliverable:** Production-ready system

---

## 🛠️ Technology Stack

### Core Technologies
- **Python 3.10+**
- **SQLite** (existing)
- **BeautifulSoup4** (HTML parsing)
- **Requests** / **Playwright** (HTTP/scraping)
- **OpenAI API** (LLM)
- **sentence-transformers** (embeddings)
- **scikit-learn** (clustering)

### Optional Enhancements
- **Redis** (caching for SERP results)
- **Celery** (async task queue for scraping)
- **Postgres** (if scaling beyond SQLite)
- **Docker** (containerization for deployment)

---

## 🎯 Next Steps

### This Week
1. **Get budget approval** (~$10 for initial test)
2. **Set up OpenAI API key**
3. **Create database schema extensions** (run migration)
4. **Build context scraper** (test on 10 links)

### Next Week
1. **Build entity extractor** (test on scraped links)
2. **Manual validation** (check 20 extractions for accuracy)
3. **Iterate on prompts** (improve LLM output quality)

### This Month
1. **Complete Pillar 1** (context + entities for all links)
2. **Start Pillar 2** (SERP analysis for 5 URLs)
3. **Demo to team** (show semantic insights)

---

**The semantic future of link building is here. Let's build it.** 🚀

---

*Document created: 2025-11-12*
*Version: 1.0*
*Status: Ready for implementation*
