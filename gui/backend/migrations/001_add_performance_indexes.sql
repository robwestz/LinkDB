-- Migration: Add performance indexes to customer_history table
-- Purpose: Dramatically improve query performance for common operations
-- Created: 2025-11-12
-- Priority: P1 (High)

-- Index on customer_id (most frequently queried field)
-- Speeds up: All customer-specific queries
-- Estimated improvement: 50-80% faster on large datasets
CREATE INDEX IF NOT EXISTS idx_customer_id
ON customer_history(customer_id);

-- Index on published_at (date range queries)
-- Speeds up: Temporal analysis, date filtering
-- Estimated improvement: 70-90% faster on date range queries
CREATE INDEX IF NOT EXISTS idx_published_at
ON customer_history(published_at);

-- Index on pub_domain (domain analysis)
-- Speeds up: Domain source analysis, domain-based filtering
-- Estimated improvement: 60-80% faster on domain queries
CREATE INDEX IF NOT EXISTS idx_pub_domain
ON customer_history(pub_domain);

-- Composite index on customer_id + published_at
-- Speeds up: Customer analysis with date ranges (most common query pattern)
-- Estimated improvement: 80-95% faster on combined queries
CREATE INDEX IF NOT EXISTS idx_customer_date
ON customer_history(customer_id, published_at);

-- Index on target_url
-- Speeds up: Target URL analysis, deep linking ratio calculations
-- Estimated improvement: 60-80% faster on URL analysis
CREATE INDEX IF NOT EXISTS idx_target_url
ON customer_history(target_url);

-- Composite index on customer_id + pub_domain
-- Speeds up: Domain source analysis per customer
-- Estimated improvement: 70-85% faster on domain analysis queries
CREATE INDEX IF NOT EXISTS idx_customer_domain
ON customer_history(customer_id, pub_domain);

-- Index on anchor_text (for search and frequency analysis)
-- Speeds up: Anchor text search, frequency analysis
-- Estimated improvement: 50-70% faster on anchor searches
CREATE INDEX IF NOT EXISTS idx_anchor_text
ON customer_history(anchor_text);

-- Analyze table to update statistics for query planner
ANALYZE customer_history;

-- Verification queries to check index usage:
-- EXPLAIN QUERY PLAN SELECT * FROM customer_history WHERE customer_id = 117;
-- EXPLAIN QUERY PLAN SELECT * FROM customer_history WHERE published_at >= '2024-01-01';
-- EXPLAIN QUERY PLAN SELECT * FROM customer_history WHERE customer_id = 117 AND published_at >= '2024-01-01';
