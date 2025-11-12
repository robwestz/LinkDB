PRAGMA foreign_keys = ON;
PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS customers (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  canonical_root TEXT UNIQUE NOT NULL,
  brand TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS links_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,
  pub_page_url TEXT NOT NULL,
  pub_domain TEXT,
  target_url TEXT NOT NULL,
  target_domain TEXT,
  anchor_text TEXT,
  link_type TEXT,
  language TEXT,
  published_at TEXT,
  topic_tags TEXT,
  context_excerpt TEXT,
  anchor_type TEXT,
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_links_customer_id ON links_history(customer_id);
CREATE INDEX IF NOT EXISTS idx_links_pub_domain ON links_history(pub_domain);
CREATE INDEX IF NOT EXISTS idx_links_target_domain ON links_history(target_domain);

/* Förebygg dubletter vid upprepad import: “naturlig nyckel” */
CREATE UNIQUE INDEX IF NOT EXISTS uq_links_history_natural
ON links_history (
  customer_id,
  pub_page_url,
  target_url,
  anchor_text,
  published_at
);
