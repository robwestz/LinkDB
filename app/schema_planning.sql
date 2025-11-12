-- Schema för intelligent länkplanering
-- Version: 1.0
-- Skapad: 2025-11-05

-- ============================================================================
-- PLANERING - Huvudtabeller
-- ============================================================================

-- Länkplaner (en plan kan innehålla många länkar)
CREATE TABLE IF NOT EXISTS link_plans (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_name TEXT NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    created_by TEXT,
    status TEXT DEFAULT 'draft' CHECK(status IN ('draft', 'approved', 'in_progress', 'completed', 'cancelled')),
    total_links INTEGER DEFAULT 0,
    semantic_strategy TEXT, -- Vilken strategi användes
    google_sheet_url TEXT, -- Länk till planeringsdokument
    notes TEXT
);

-- Enskilda länkningar i planen
CREATE TABLE IF NOT EXISTS planned_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL REFERENCES link_plans(id) ON DELETE CASCADE,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    target_url TEXT NOT NULL,
    target_domain TEXT,
    anchor_text TEXT NOT NULL,
    anchor_type TEXT CHECK(anchor_type IN ('exact', 'partial', 'branded', 'generic', 'lsi', 'naked_url')),
    semantic_cluster_id INTEGER REFERENCES semantic_clusters(id),
    topic TEXT,
    priority_score REAL DEFAULT 0,
    reasoning TEXT, -- Förklaring varför denna länk/ankar valdes
    status TEXT DEFAULT 'planned' CHECK(status IN ('planned', 'published', 'cancelled', 'failed')),
    published_at DATETIME,
    pub_page_url TEXT, -- Fylls i när länken publicerats
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- SEMANTISK ANALYS
-- ============================================================================

-- Semantiska kluster (grupper av relaterade målsidor)
CREATE TABLE IF NOT EXISTS semantic_clusters (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    plan_id INTEGER REFERENCES link_plans(id),
    cluster_name TEXT NOT NULL,
    topic TEXT NOT NULL,
    description TEXT,
    keywords TEXT, -- JSON array: ["keyword1", "keyword2"]
    target_urls TEXT, -- JSON array: ["url1", "url2"]
    link_count INTEGER DEFAULT 0,
    priority_score REAL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Extraherade entiteter från målsidor
CREATE TABLE IF NOT EXISTS entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    target_url TEXT NOT NULL,
    entity_text TEXT NOT NULL,
    entity_type TEXT, -- PERSON, ORG, PRODUCT, LOCATION, KEYWORD, etc.
    relevance_score REAL, -- 0-1, hur relevant är entiteten
    frequency INTEGER, -- Hur många gånger förekommer den
    context TEXT, -- Kontext där entiteten hittades
    extracted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(target_url, entity_text, entity_type)
);

-- Relaterade fraser (semantiskt liknande sökfraser)
CREATE TABLE IF NOT EXISTS related_phrases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    base_phrase TEXT NOT NULL,
    related_phrase TEXT NOT NULL,
    similarity_score REAL, -- 0-1, semantisk likhet
    phrase_type TEXT, -- synonym, related, lsi, etc.
    source TEXT, -- Var kom relationen från (ML model, manual, etc.)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(customer_id, base_phrase, related_phrase)
);

-- ============================================================================
-- ANALYS & METRICS
-- ============================================================================

-- Historisk analys per kund
CREATE TABLE IF NOT EXISTS customer_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    analysis_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_links INTEGER DEFAULT 0,
    unique_pub_domains INTEGER DEFAULT 0,
    avg_links_per_month REAL,
    most_common_anchor_type TEXT,
    top_target_domains TEXT, -- JSON array
    link_velocity REAL, -- Länkar per månad
    anchor_diversity_score REAL, -- 0-1
    semantic_coherence_score REAL, -- 0-1
    notes TEXT
);

-- Metrics för planer
CREATE TABLE IF NOT EXISTS planning_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL REFERENCES link_plans(id),
    metric_name TEXT NOT NULL,
    metric_value REAL,
    metric_unit TEXT,
    description TEXT,
    calculated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Anchor text distribution per plan
CREATE TABLE IF NOT EXISTS anchor_distribution (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    plan_id INTEGER NOT NULL REFERENCES link_plans(id),
    anchor_type TEXT NOT NULL,
    count INTEGER DEFAULT 0,
    percentage REAL,
    target_percentage REAL, -- Önskad fördelning
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- MÅLSIDOR & INNEHÅLL
-- ============================================================================

-- Målsidor med metadata
CREATE TABLE IF NOT EXISTS target_pages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    url TEXT NOT NULL UNIQUE,
    domain TEXT,
    title TEXT,
    meta_description TEXT,
    main_topic TEXT,
    content_type TEXT, -- article, product, category, home, etc.
    word_count INTEGER,
    scraped_content TEXT, -- Full text content
    scraped_at DATETIME,
    last_analyzed DATETIME,
    is_active BOOLEAN DEFAULT 1,
    priority INTEGER DEFAULT 0,
    notes TEXT
);

-- Nyckelord per målsida
CREATE TABLE IF NOT EXISTS page_keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_id INTEGER NOT NULL REFERENCES target_pages(id) ON DELETE CASCADE,
    keyword TEXT NOT NULL,
    keyword_type TEXT, -- primary, secondary, lsi
    tf_idf_score REAL,
    position INTEGER, -- Position på sidan
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(page_id, keyword)
);

-- ============================================================================
-- STRATEGIER & KONFIGURATION
-- ============================================================================

-- Planering strategier
CREATE TABLE IF NOT EXISTS planning_strategies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    strategy_name TEXT NOT NULL UNIQUE,
    description TEXT,
    link_count_min INTEGER, -- Minsta antal länkar strategin gäller för
    link_count_max INTEGER, -- Största antal länkar
    anchor_distribution TEXT, -- JSON: {"exact": 15, "partial": 35, ...}
    semantic_clustering BOOLEAN DEFAULT 1,
    topical_authority_focus BOOLEAN DEFAULT 1,
    diversification_level TEXT CHECK(diversification_level IN ('low', 'medium', 'high')),
    config TEXT, -- JSON med ytterligare konfiguration
    is_active BOOLEAN DEFAULT 1,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Customer-specifika inställningar
CREATE TABLE IF NOT EXISTS customer_planning_settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL REFERENCES customers(id) UNIQUE,
    preferred_strategy_id INTEGER REFERENCES planning_strategies(id),
    anchor_preferences TEXT, -- JSON med preferenser
    forbidden_anchor_patterns TEXT, -- JSON array med förbjudna mönster
    priority_keywords TEXT, -- JSON array med prioriterade nyckelord
    notes TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================================
-- INDEXES för prestanda
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_planned_links_plan ON planned_links(plan_id);
CREATE INDEX IF NOT EXISTS idx_planned_links_customer ON planned_links(customer_id);
CREATE INDEX IF NOT EXISTS idx_planned_links_status ON planned_links(status);
CREATE INDEX IF NOT EXISTS idx_planned_links_cluster ON planned_links(semantic_cluster_id);

CREATE INDEX IF NOT EXISTS idx_semantic_clusters_customer ON semantic_clusters(customer_id);
CREATE INDEX IF NOT EXISTS idx_semantic_clusters_plan ON semantic_clusters(plan_id);

CREATE INDEX IF NOT EXISTS idx_entities_customer ON entities(customer_id);
CREATE INDEX IF NOT EXISTS idx_entities_url ON entities(target_url);
CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(entity_type);

CREATE INDEX IF NOT EXISTS idx_related_phrases_customer ON related_phrases(customer_id);
CREATE INDEX IF NOT EXISTS idx_related_phrases_base ON related_phrases(base_phrase);

CREATE INDEX IF NOT EXISTS idx_target_pages_customer ON target_pages(customer_id);
CREATE INDEX IF NOT EXISTS idx_target_pages_url ON target_pages(url);

CREATE INDEX IF NOT EXISTS idx_page_keywords_page ON page_keywords(page_id);
CREATE INDEX IF NOT EXISTS idx_page_keywords_keyword ON page_keywords(keyword);

-- ============================================================================
-- TRIGGERS för automatisk uppdatering
-- ============================================================================

-- Uppdatera updated_at på link_plans
CREATE TRIGGER IF NOT EXISTS update_link_plans_timestamp
AFTER UPDATE ON link_plans
BEGIN
    UPDATE link_plans SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Uppdatera updated_at på planned_links
CREATE TRIGGER IF NOT EXISTS update_planned_links_timestamp
AFTER UPDATE ON planned_links
BEGIN
    UPDATE planned_links SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;

-- Räkna total_links i plan när planned_links läggs till
CREATE TRIGGER IF NOT EXISTS count_links_in_plan_insert
AFTER INSERT ON planned_links
BEGIN
    UPDATE link_plans
    SET total_links = (SELECT COUNT(*) FROM planned_links WHERE plan_id = NEW.plan_id)
    WHERE id = NEW.plan_id;
END;

-- Räkna total_links i plan när planned_links tas bort
CREATE TRIGGER IF NOT EXISTS count_links_in_plan_delete
AFTER DELETE ON planned_links
BEGIN
    UPDATE link_plans
    SET total_links = (SELECT COUNT(*) FROM planned_links WHERE plan_id = OLD.plan_id)
    WHERE id = OLD.plan_id;
END;

-- ============================================================================
-- VIEWS för enkel dataåtkomst
-- ============================================================================

-- Översikt av planer med statistik
CREATE VIEW IF NOT EXISTS v_plan_overview AS
SELECT
    lp.id,
    lp.plan_name,
    lp.status,
    lp.created_at,
    lp.total_links,
    lp.semantic_strategy,
    COUNT(DISTINCT pl.customer_id) as customer_count,
    COUNT(DISTINCT pl.semantic_cluster_id) as cluster_count,
    AVG(pl.priority_score) as avg_priority,
    COUNT(CASE WHEN pl.status = 'published' THEN 1 END) as published_count,
    COUNT(CASE WHEN pl.status = 'planned' THEN 1 END) as planned_count
FROM link_plans lp
LEFT JOIN planned_links pl ON lp.id = pl.plan_id
GROUP BY lp.id;

-- Anchor distribution per plan
CREATE VIEW IF NOT EXISTS v_anchor_type_distribution AS
SELECT
    pl.plan_id,
    pl.anchor_type,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY pl.plan_id), 2) as percentage
FROM planned_links pl
WHERE pl.status != 'cancelled'
GROUP BY pl.plan_id, pl.anchor_type;

-- Customer metrics
CREATE VIEW IF NOT EXISTS v_customer_planning_metrics AS
SELECT
    c.id as customer_id,
    c.canonical_root,
    c.brand,
    COUNT(DISTINCT pl.plan_id) as plan_count,
    COUNT(pl.id) as total_planned_links,
    COUNT(CASE WHEN pl.status = 'published' THEN 1 END) as published_links,
    COUNT(DISTINCT sc.id) as semantic_clusters,
    AVG(pl.priority_score) as avg_priority
FROM customers c
LEFT JOIN planned_links pl ON c.id = pl.customer_id
LEFT JOIN semantic_clusters sc ON c.id = sc.customer_id
GROUP BY c.id;

