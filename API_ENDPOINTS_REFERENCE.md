# LinkDB API Endpoints - Complete Reference

## 📚 Table of Contents

1. [Basic Endpoints](#basic-endpoints)
2. [Advanced Analysis Endpoints](#advanced-analysis-endpoints)
3. [CRUD Operations](#crud-operations)
4. [AI Endpoints](#ai-endpoints)
5. [Usage Examples](#usage-examples)

---

## 🔹 Basic Endpoints

### Health Check
```
GET /health
```
Response:
```json
{
  "status": "healthy",
  "service": "LinkDB Analytics API"
}
```

### Get All Customers
```
GET /api/customers
```
Response:
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "canonical_root": "example.com",
      "brand": "Example Brand",
      "total_links": 156,
      "health_score": 78.5
    }
  ]
}
```

### Dashboard Metrics
```
GET /api/dashboard/metrics
```
Response:
```json
{
  "success": true,
  "data": {
    "total_customers": 42,
    "total_links": 3245,
    "avg_health": 75.2,
    "top_performers": [
      {"domain": "example.com", "links": 156}
    ]
  }
}
```

### Customer Analysis
```
GET /api/customers/{customer_id}/analysis
```
Response: Complete analysis with anchor quality, temporal patterns, domain quality.

### Get Links (Paginated)
```
GET /api/links?offset=0&limit=50&search=keyword&customer_id=1
```
Query params:
- `offset`: Starting position (default: 0)
- `limit`: Number of results (default: 50, max: 100)
- `search`: Search term (optional)
- `customer_id`: Filter by customer (optional)

### Competitive Overview
```
GET /api/competitive/overview
```
Response: Industry benchmarking data.

---

## 🚀 Advanced Analysis Endpoints

### 1. Anchor Frequency Analysis
```
GET /api/advanced/customers/{customer_id}/anchor-frequency
```

**Query Parameters:**
- `from_date`: Start date (YYYY-MM) - Optional
- `to_date`: End date (YYYY-MM) - Optional
- `limit`: Max results (default: 100, max: 500)

**Example:**
```
GET /api/advanced/customers/1/anchor-frequency?from_date=2024-01&to_date=2024-03&limit=50
```

**Response:**
```json
{
  "success": true,
  "data": {
    "anchors": [
      {
        "anchor_text": "best seo services",
        "frequency": 45
      },
      {
        "anchor_text": "professional seo",
        "frequency": 38
      }
    ],
    "statistics": {
      "total_links": 296,
      "unique_anchors": 87,
      "date_range": {
        "from": "2024-01",
        "to": "2024-03"
      }
    }
  }
}
```

**Use Case:** Identify most used anchor texts, detect over-optimization.

---

### 2. Word Frequency in Anchors
```
GET /api/advanced/customers/{customer_id}/word-frequency
```

**Query Parameters:**
- `from_date`: Start date (YYYY-MM) - Optional
- `to_date`: End date (YYYY-MM) - Optional
- `min_length`: Minimum word length (default: 3)
- `limit`: Max results (default: 100, max: 500)

**Example:**
```
GET /api/advanced/customers/1/word-frequency?from_date=2024-01&to_date=2024-06&min_length=4&limit=100
```

**Response:**
```json
{
  "success": true,
  "data": {
    "words": [
      {
        "word": "seo",
        "frequency": 145,
        "percentage": 48.99
      },
      {
        "word": "services",
        "frequency": 89,
        "percentage": 30.07
      }
    ],
    "statistics": {
      "total_anchor_texts": 296,
      "unique_words": 324,
      "top_words_shown": 100,
      "date_range": {
        "from": "2024-01",
        "to": "2024-06"
      }
    }
  }
}
```

**Use Case:** Find overused keywords, analyze language patterns.

---

### 3. Search Anchor Texts
```
GET /api/advanced/customers/{customer_id}/anchor-search
```

**Query Parameters:**
- `search_term`: Word or phrase to search for (required)
- `from_date`: Start date (YYYY-MM) - Optional
- `to_date`: End date (YYYY-MM) - Optional
- `case_sensitive`: Boolean (default: false)

**Example:**
```
GET /api/advanced/customers/1/anchor-search?search_term=seo&case_sensitive=false
```

**Response:**
```json
{
  "success": true,
  "data": {
    "matches": [
      {
        "anchor_text": "best seo services",
        "pub_domain": "example.com",
        "target_url": "site.com/services",
        "published_at": "2024-03-15"
      }
    ],
    "statistics": {
      "total_matches": 23,
      "search_term": "seo",
      "case_sensitive": false,
      "date_range": {
        "from": null,
        "to": null
      }
    }
  }
}
```

**Use Case:** Find all links containing specific keywords, audit anchor text usage.

---

### 4. Target URL Analysis
```
GET /api/advanced/customers/{customer_id}/target-url-analysis
```

**Query Parameters:**
- `from_date`: Start date (YYYY-MM) - Optional
- `to_date`: End date (YYYY-MM) - Optional
- `limit`: Max results (default: 50, max: 200)

**Example:**
```
GET /api/advanced/customers/1/target-url-analysis?limit=50
```

**Response:**
```json
{
  "success": true,
  "data": {
    "target_urls": [
      {
        "target_url": "example.com/",
        "link_count": 52,
        "is_homepage": true
      },
      {
        "target_url": "example.com/blog/seo-guide",
        "link_count": 18,
        "is_homepage": false
      }
    ],
    "statistics": {
      "total_links": 147,
      "unique_urls": 48,
      "homepage_links": 52,
      "deep_links": 95,
      "deep_linking_ratio": 64.63,
      "date_range": {
        "from": null,
        "to": null
      }
    }
  }
}
```

**Use Case:** Understand which pages attract links, measure deep linking strategy.

---

### 5. Link Velocity
```
GET /api/advanced/customers/{customer_id}/link-velocity
```

**Query Parameters:**
- `from_date`: Start date (YYYY-MM) - Optional
- `to_date`: End date (YYYY-MM) - Optional

**Example:**
```
GET /api/advanced/customers/1/link-velocity?from_date=2023-01&to_date=2024-03
```

**Response:**
```json
{
  "success": true,
  "data": {
    "monthly_data": [
      {
        "month": "2023-01",
        "link_count": 8
      },
      {
        "month": "2023-02",
        "link_count": 12
      },
      {
        "month": "2024-03",
        "link_count": 42
      }
    ],
    "statistics": {
      "total_months": 15,
      "avg_links_per_month": 24.53,
      "avg_change_per_month": 2.27,
      "trend": "accelerating",
      "date_range": {
        "from": "2023-01",
        "to": "2024-03"
      }
    }
  }
}
```

**Trend Values:**
- `accelerating`: Positive growth (>2 links/month increase)
- `stable`: Steady state (-2 to +2 links/month)
- `decelerating`: Negative growth (<-2 links/month decrease)
- `insufficient_data`: Less than 2 months of data

**Use Case:** Track link building campaigns, detect unnatural velocity spikes.

---

### 6. Domain Sources Analysis
```
GET /api/advanced/customers/{customer_id}/domain-sources
```

**Query Parameters:**
- `from_date`: Start date (YYYY-MM) - Optional
- `to_date`: End date (YYYY-MM) - Optional
- `limit`: Max results (default: 50, max: 200)

**Example:**
```
GET /api/advanced/customers/1/domain-sources?limit=100
```

**Response:**
```json
{
  "success": true,
  "data": {
    "domains": [
      {
        "pub_domain": "blog.example.com",
        "link_count": 8,
        "first_link": "2023-05-12",
        "latest_link": "2024-03-10",
        "is_new_domain": false
      },
      {
        "pub_domain": "news.site.io",
        "link_count": 1,
        "first_link": "2024-03-18",
        "latest_link": "2024-03-18",
        "is_new_domain": true
      }
    ],
    "statistics": {
      "total_domains": 156,
      "new_domains": 42,
      "returning_domains": 114,
      "new_domain_ratio": 26.92,
      "date_range": {
        "from": null,
        "to": null
      }
    }
  }
}
```

**Use Case:** Identify new link sources, track domain relationship building.

---

### 7. Period Comparison
```
GET /api/advanced/customers/{customer_id}/comparison
```

**Query Parameters (all required):**
- `period1_from`: Period 1 start (YYYY-MM)
- `period1_to`: Period 1 end (YYYY-MM)
- `period2_from`: Period 2 start (YYYY-MM)
- `period2_to`: Period 2 end (YYYY-MM)

**Example:**
```
GET /api/advanced/customers/1/comparison?period1_from=2024-01&period1_to=2024-03&period2_from=2024-04&period2_to=2024-06
```

**Response:**
```json
{
  "success": true,
  "data": {
    "period1": {
      "total_links": 72,
      "unique_domains": 34,
      "unique_target_urls": 18,
      "date_range": {
        "from": "2024-01",
        "to": "2024-03"
      }
    },
    "period2": {
      "total_links": 95,
      "unique_domains": 48,
      "unique_target_urls": 22,
      "date_range": {
        "from": "2024-04",
        "to": "2024-06"
      }
    },
    "changes": {
      "total_links_change": 23,
      "total_links_change_percent": 31.94,
      "unique_domains_change": 14,
      "unique_domains_change_percent": 41.18,
      "unique_urls_change": 4,
      "unique_urls_change_percent": 22.22
    }
  }
}
```

**Use Case:** Measure campaign effectiveness, before/after analysis.

---

## 🛠️ CRUD Operations

### Create Link
```
POST /api/links/
```

**Request Body:**
```json
{
  "customer_id": 1,
  "canonical_root": "example.com",
  "brand": "Example Brand",
  "pub_domain": "blog.site.com",
  "target_url": "https://example.com/services",
  "anchor_text": "professional seo services",
  "published_at": "2024-03-15"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Link created successfully",
  "data": {
    "id": 3246,
    "customer_id": 1,
    "canonical_root": "example.com",
    "brand": "Example Brand",
    "pub_domain": "blog.site.com",
    "target_url": "https://example.com/services",
    "anchor_text": "professional seo services",
    "published_at": "2024-03-15"
  }
}
```

---

### Read Link
```
GET /api/links/{link_id}
```

**Example:**
```
GET /api/links/3246
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": 3246,
    "customer_id": 1,
    "canonical_root": "example.com",
    "brand": "Example Brand",
    "pub_domain": "blog.site.com",
    "target_url": "https://example.com/services",
    "anchor_text": "professional seo services",
    "published_at": "2024-03-15"
  }
}
```

---

### Update Link
```
PUT /api/links/{link_id}
```

**Request Body (partial update):**
```json
{
  "anchor_text": "best seo services",
  "published_at": "2024-03-16"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Link updated successfully",
  "data": {
    "id": 3246,
    "customer_id": 1,
    "canonical_root": "example.com",
    "brand": "Example Brand",
    "pub_domain": "blog.site.com",
    "target_url": "https://example.com/services",
    "anchor_text": "best seo services",
    "published_at": "2024-03-16"
  }
}
```

---

### Delete Link
```
DELETE /api/links/{link_id}
```

**Example:**
```
DELETE /api/links/3246
```

**Response:**
```json
{
  "success": true,
  "message": "Link 3246 deleted successfully"
}
```

---

### Bulk Delete Links
```
POST /api/links/bulk-delete
```

**Request Body:**
```json
[1, 2, 3, 4, 5]
```

**Response:**
```json
{
  "success": true,
  "message": "Deleted 5 link(s)",
  "data": {
    "deleted_count": 5
  }
}
```

---

## 🤖 AI Endpoints

### AI Chat
```
POST /api/ai/chat
```

**Request Body:**
```json
{
  "messages": [
    {
      "role": "user",
      "content": "How can I improve my anchor text distribution?"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "response": "To improve your anchor text distribution..."
  }
}
```

### Get Customer Insights
```
GET /api/ai/insights/{customer_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "insights": [
      "Your exact match ratio is within healthy range (22%)",
      "Strong domain diversity with 156 unique sources"
    ]
  }
}
```

### Get Recommendations
```
GET /api/ai/recommendations/{customer_id}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "recommendations": [
      "Consider increasing branded anchor texts",
      "Target more deep links to product pages"
    ]
  }
}
```

---

## 📖 Usage Examples

### Example 1: Date-Filtered Anchor Analysis

**Scenario:** Analyze anchor texts used in Q1 2024

```bash
# Get anchor frequency for Q1 2024
curl "http://localhost:8000/api/advanced/customers/1/anchor-frequency?from_date=2024-01&to_date=2024-03&limit=50"

# Get word frequency for same period
curl "http://localhost:8000/api/advanced/customers/1/word-frequency?from_date=2024-01&to_date=2024-03&min_length=4&limit=100"
```

### Example 2: Campaign Effectiveness

**Scenario:** Compare link building before and after campaign

```bash
# Before campaign (Jan-Mar)
# After campaign (Apr-Jun)
curl "http://localhost:8000/api/advanced/customers/1/comparison?period1_from=2024-01&period1_to=2024-03&period2_from=2024-04&period2_to=2024-06"
```

### Example 3: Link Velocity Tracking

**Scenario:** Monitor link acquisition speed over the year

```bash
curl "http://localhost:8000/api/advanced/customers/1/link-velocity?from_date=2023-01&to_date=2024-12"
```

### Example 4: Adding a New Link

**Scenario:** Manually add a discovered link

```bash
curl -X POST "http://localhost:8000/api/links/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "canonical_root": "example.com",
    "brand": "Example Brand",
    "pub_domain": "newssite.com",
    "target_url": "https://example.com/blog/new-post",
    "anchor_text": "check out this guide",
    "published_at": "2024-11-12"
  }'
```

### Example 5: Search for Over-Optimization

**Scenario:** Find all exact match anchors

```bash
curl "http://localhost:8000/api/advanced/customers/1/anchor-search?search_term=best%20seo%20services&case_sensitive=false"
```

### Example 6: Deep Linking Analysis

**Scenario:** Check homepage vs content page links

```bash
curl "http://localhost:8000/api/advanced/customers/1/target-url-analysis?limit=100"
```

---

## 🔧 Testing All Endpoints

Use this script to test all endpoints:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"
CUSTOMER_ID=1

echo "Testing Basic Endpoints..."
curl -s "$BASE_URL/health" | jq
curl -s "$BASE_URL/api/customers" | jq

echo -e "\nTesting Advanced Analysis..."
curl -s "$BASE_URL/api/advanced/customers/$CUSTOMER_ID/anchor-frequency?limit=10" | jq
curl -s "$BASE_URL/api/advanced/customers/$CUSTOMER_ID/word-frequency?limit=10" | jq
curl -s "$BASE_URL/api/advanced/customers/$CUSTOMER_ID/target-url-analysis?limit=10" | jq
curl -s "$BASE_URL/api/advanced/customers/$CUSTOMER_ID/link-velocity" | jq
curl -s "$BASE_URL/api/advanced/customers/$CUSTOMER_ID/domain-sources?limit=10" | jq

echo -e "\nTesting Period Comparison..."
curl -s "$BASE_URL/api/advanced/customers/$CUSTOMER_ID/comparison?period1_from=2024-01&period1_to=2024-03&period2_from=2024-04&period2_to=2024-06" | jq

echo -e "\nAll tests completed!"
```

---

## 📊 Error Responses

All endpoints return consistent error format:

**400 Bad Request:**
```json
{
  "detail": "Invalid date format. Use YYYY-MM"
}
```

**404 Not Found:**
```json
{
  "detail": "Customer with ID 999 not found"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Error fetching anchor frequency: [error details]"
}
```

---

## 🎯 Best Practices

1. **Date Filtering:**
   - Always use YYYY-MM format
   - Date ranges are inclusive for start, exclusive for end
   - Example: 2024-01 to 2024-03 includes Jan, Feb, March 1-31

2. **Pagination:**
   - Use `limit` to control response size
   - Maximum limits vary by endpoint (100-500)
   - Use `offset` for pagination in basic endpoints

3. **Performance:**
   - Date-filtered queries are faster than full scans
   - Limit results to what you need
   - Cache responses when appropriate

4. **Data Integrity:**
   - Validate dates before submission (YYYY-MM-DD for CRUD)
   - Use bulk operations for multiple changes
   - Always confirm before bulk deletes

---

## 📝 Notes

- All dates in database are stored as YYYY-MM-DD
- Query parameters use YYYY-MM (month precision)
- All percentage values are 0-100 (not 0-1)
- Statistics are calculated in real-time
- CRUD operations modify the database immediately

---

**API Version:** 1.0
**Last Updated:** 2024-11-12
**Backend:** FastAPI (Python)
**Database:** SQLite
