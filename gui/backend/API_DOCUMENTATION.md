# LinkDB Backend API Documentation

## Overview

The LinkDB Backend API is a FastAPI-based REST API that exposes all LinkDB analyzers and provides comprehensive link analysis endpoints for the LinkDB GUI application.

**Base URL:** `http://localhost:8000`
**API Version:** 1.0.0
**Interactive Docs:** `http://localhost:8000/docs` (Swagger UI)
**Alternative Docs:** `http://localhost:8000/redoc` (ReDoc)

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Authentication](#authentication)
3. [Response Format](#response-format)
4. [Error Handling](#error-handling)
5. [Endpoints](#endpoints)
   - [Health & Info](#health--info-endpoints)
   - [Customers](#customer-endpoints)
   - [Competitive Analysis](#competitive-analysis-endpoints)
   - [Dashboard](#dashboard-endpoints)
6. [Data Models](#data-models)
7. [Examples](#examples)

---

## Getting Started

### Installation

1. Install dependencies:
```bash
cd gui/backend
pip install -r requirements.txt
```

2. Ensure database exists at:
```
/home/user/LinkDB/data/output/linkops_history.db
```

3. Start the server:
```bash
python app.py
```

Or using uvicorn directly:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

### CORS Configuration

The API is configured with permissive CORS settings for development. All origins, methods, and headers are allowed. **For production, restrict `allow_origins` to specific domains.**

---

## Authentication

Currently, the API does not require authentication. This may be added in future versions.

---

## Response Format

### Success Response

All successful responses follow this structure:

```json
{
  "success": true,
  "data": {
    // Response data here
  }
}
```

### Error Response

All error responses follow this structure:

```json
{
  "success": false,
  "error": "Error message",
  "detail": "Detailed error information (optional)"
}
```

---

## Error Handling

### HTTP Status Codes

- `200 OK` - Request successful
- `404 Not Found` - Resource not found (customer, data, etc.)
- `422 Unprocessable Entity` - Validation error (invalid parameters)
- `500 Internal Server Error` - Server error (database issues, analyzer failures)

### Common Error Scenarios

1. **Database Not Found** (500):
   - Occurs when `linkops_history.db` doesn't exist
   - Solution: Initialize database using LinkDB tools

2. **Customer Not Found** (404):
   - Occurs when requesting a non-existent customer ID
   - Solution: Use `/api/customers` to list valid customer IDs

3. **No Data Available** (404):
   - Occurs when a customer has no link data
   - Solution: Import data for the customer first

---

## Endpoints

### Health & Info Endpoints

#### `GET /`
Root endpoint with API information.

**Response:**
```json
{
  "name": "LinkDB Analytics API",
  "version": "1.0.0",
  "status": "active",
  "endpoints": {
    "docs": "/docs",
    "health": "/health",
    "customers": "/api/customers",
    "competitive": "/api/competitive",
    "dashboard": "/api/dashboard"
  }
}
```

#### `GET /health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "database": {
    "path": "/home/user/LinkDB/data/output/linkops_history.db",
    "exists": true
  },
  "api_version": "1.0.0"
}
```

**Status values:**
- `healthy` - Database exists and accessible
- `degraded` - Database not found

---

### Customer Endpoints

#### `GET /api/customers`
List all customers with basic information.

**Response Model:** `List[CustomerBasic]`

**Response:**
```json
[
  {
    "id": 117,
    "canonical_root": "bethard.com",
    "brand": "Bethard",
    "total_links": 245
  },
  {
    "id": 118,
    "canonical_root": "example.com",
    "brand": "Example Brand",
    "total_links": 180
  }
]
```

**Sorting:** Results are sorted by `total_links DESC`, then `canonical_root ASC`

---

#### `GET /api/customers/{customer_id}`
Get detailed information for a specific customer.

**Parameters:**
- `customer_id` (path, required): Customer ID

**Response Model:** `CustomerDetail`

**Response:**
```json
{
  "id": 117,
  "canonical_root": "bethard.com",
  "brand": "Bethard",
  "created_at": "2024-01-15T10:30:00",
  "total_links": 245,
  "unique_pub_domains": 156,
  "unique_target_urls": 89,
  "links_per_month": 40.8
}
```

**Errors:**
- `404` - Customer not found

---

#### `GET /api/customers/{customer_id}/analysis`
Get complete analysis for a customer (runs all analyzers).

**Parameters:**
- `customer_id` (path, required): Customer ID

**Response:**
```json
{
  "success": true,
  "data": {
    "customer_id": 117,
    "canonical_root": "bethard.com",
    "brand": "Bethard",
    "overall_score": 78.5,
    "link_history": {
      "total_links": 245,
      "unique_pub_domains": 156,
      "unique_target_urls": 89,
      "links_per_month": 40.8,
      "primary_strategy": "Diverse anchor strategy with focus on branded links",
      "recommendations": [
        "Continue diversification strategy",
        "Focus on quality domains"
      ],
      "most_common_anchors": [
        ["Bethard", 45],
        ["casino online", 23]
      ],
      "most_linked_urls": [
        ["https://bethard.com/casino", 56],
        ["https://bethard.com/sports", 34]
      ]
    },
    "anchor_quality": {
      "quality_score": 82.3,
      "diversity_score": 75.6,
      "over_optimization_risk": "low",
      "shannon_entropy": 4.52,
      "exact_match_ratio": 15.2,
      "branded_ratio": 42.8,
      "commercial_keywords_ratio": 18.5,
      "warnings": [
        "✅ Anchor profile looks natural and diverse"
      ],
      "top_anchors": [
        ["Bethard", 45],
        ["casino", 23]
      ]
    },
    "temporal_patterns": {
      "health_score": 85.2,
      "links_per_month": 40.8,
      "velocity_trend": "stable",
      "consistency_score": 78.4,
      "monthly_distribution": {
        "2024-10": 42,
        "2024-09": 38
      },
      "has_unnatural_spikes": false,
      "warnings": [],
      "insights": [
        "✅ Consistent link building velocity",
        "📊 Natural temporal distribution"
      ]
    },
    "domain_quality": {
      "quality_score": 68.2,
      "unique_domains": 156,
      "diversity_score": 63.7,
      "cross_linking_score": 12.5,
      "top_tlds": [
        ["com", 98],
        ["se", 34]
      ],
      "geographic_diversity": {
        "Commercial": 98,
        "Sweden": 34
      },
      "warnings": [
        "✅ Domain profile looks natural and varied"
      ],
      "insights": [
        "✅ Excellent domain diversity (63.7/100)",
        "🌍 Geographic spread: Commercial (98), Sweden (34)"
      ],
      "top_domains": [
        ["example.com", 12],
        ["sample-site.com", 8]
      ]
    }
  }
}
```

**Analysis Components:**
1. **link_history** - Historical link data and patterns
2. **anchor_quality** - Anchor text diversity and naturality analysis
3. **temporal_patterns** - Time-based patterns and consistency
4. **domain_quality** - Publishing domain quality assessment

**Errors:**
- `404` - Customer not found or has no data
- `500` - Analysis error

---

#### `GET /api/customers/{customer_id}/links`
Get link history for a customer with pagination.

**Parameters:**
- `customer_id` (path, required): Customer ID
- `limit` (query, optional): Max links to return (1-1000, default: 100)
- `offset` (query, optional): Number of links to skip (default: 0)

**Response:**
```json
{
  "success": true,
  "data": {
    "total": 245,
    "limit": 100,
    "offset": 0,
    "links": [
      {
        "id": 1,
        "pub_page_url": "https://example.com/article",
        "pub_domain": "example.com",
        "target_url": "https://bethard.com/casino",
        "target_domain": "bethard.com",
        "anchor_text": "best casino",
        "anchor_type": "partial_match",
        "link_type": "dofollow",
        "language": "en",
        "published_at": "2024-10-15T14:30:00",
        "topic_tags": "casino,gambling",
        "created_at": "2024-10-16T08:00:00"
      }
    ]
  }
}
```

**Sorting:** Links ordered by `published_at DESC`, then `created_at DESC`

**Errors:**
- `404` - Customer not found
- `422` - Invalid pagination parameters

---

#### `GET /api/customers/{customer_id}/links/monthly`
Get links grouped by publication month.

**Parameters:**
- `customer_id` (path, required): Customer ID

**Response:**
```json
{
  "success": true,
  "data": {
    "customer_id": 117,
    "total_months": 6,
    "months": [
      {
        "year": 2024,
        "month": 10,
        "month_name": "October",
        "period": "2024-10",
        "link_count": 42,
        "unique_pub_domains": 35,
        "unique_target_urls": 18
      },
      {
        "year": 2024,
        "month": 9,
        "month_name": "September",
        "period": "2024-09",
        "link_count": 38,
        "unique_pub_domains": 32,
        "unique_target_urls": 16
      }
    ]
  }
}
```

**Sorting:** Months ordered by `year DESC`, `month DESC` (most recent first)

**Errors:**
- `404` - Customer not found

---

### Competitive Analysis Endpoints

#### `GET /api/competitive`
Get industry-wide competitive insights.

**Response:**
```json
{
  "success": true,
  "data": {
    "total_customers_analyzed": 45,
    "benchmarks": {
      "avg_total_links": 156.3,
      "median_total_links": 98.0,
      "avg_links_per_month": 26.1,
      "avg_anchor_diversity": 68.5,
      "avg_domain_diversity": 72.3
    },
    "top_performers": {
      "by_volume": [
        ["bethard.com", 245],
        ["example.com", 180]
      ],
      "by_quality": [
        ["bethard.com", 82.3],
        ["premium-site.com", 79.8]
      ],
      "by_diversity": [
        ["diverse-links.com", 91.2],
        ["bethard.com", 75.6]
      ]
    },
    "distribution": {
      "volume": {
        "0-10": 5,
        "11-25": 8,
        "26-50": 12,
        "51-100": 15,
        "100+": 5
      },
      "quality_tiers": {
        "poor (0-40)": 3,
        "fair (40-60)": 12,
        "good (60-80)": 20,
        "excellent (80-100)": 10
      }
    }
  }
}
```

**Errors:**
- `404` - No customer data found
- `500` - Analysis error

---

#### `GET /api/competitive/{customer_id}`
Compare a specific customer against industry benchmarks.

**Parameters:**
- `customer_id` (path, required): Customer ID

**Response:**
```json
{
  "success": true,
  "data": {
    "customer": "bethard.com",
    "metrics": {
      "total_links": 245,
      "unique_domains": 156,
      "anchor_diversity": 75.6,
      "domain_diversity": 63.7
    },
    "vs_industry": {
      "volume_percentile": 85.0,
      "quality_percentile": 78.0,
      "vs_avg_links": 88.7,
      "vs_median_links": 147.0
    },
    "industry_context": {
      "avg_total_links": 156.3,
      "median_total_links": 98.0
    }
  }
}
```

**Percentile Rankings:**
- `0-25`: Below average
- `25-50`: Average
- `50-75`: Above average
- `75-100`: Top performer

**Errors:**
- `404` - Customer not found
- `500` - Comparison error

---

### Dashboard Endpoints

#### `GET /api/dashboard`
Get dashboard overview data.

**Response:**
```json
{
  "success": true,
  "data": {
    "overview": {
      "total_customers": 45,
      "total_links": 7034,
      "total_pub_domains": 3421,
      "total_target_urls": 1876,
      "recent_links_30d": 342
    },
    "top_customers": [
      {
        "id": 117,
        "canonical_root": "bethard.com",
        "brand": "Bethard",
        "total_links": 245
      }
    ],
    "monthly_activity": [
      {
        "month": "2024-10",
        "link_count": 456
      },
      {
        "month": "2024-09",
        "link_count": 423
      }
    ]
  }
}
```

**Time Ranges:**
- `recent_links_30d`: Last 30 days
- `monthly_activity`: Last 6 months

---

## Data Models

### CustomerBasic
```typescript
{
  id: number;
  canonical_root: string;
  brand: string | null;
  total_links: number;
}
```

### CustomerDetail
```typescript
{
  id: number;
  canonical_root: string;
  brand: string | null;
  created_at: string | null;
  total_links: number;
  unique_pub_domains: number;
  unique_target_urls: number;
  links_per_month: number;
}
```

### LinkRecord
```typescript
{
  id: number;
  pub_page_url: string;
  pub_domain: string | null;
  target_url: string;
  target_domain: string | null;
  anchor_text: string | null;
  anchor_type: string | null;
  link_type: string | null;
  language: string | null;
  published_at: string | null;
  topic_tags: string | null;
  created_at: string | null;
}
```

---

## Examples

### Example 1: Get Customer List

```bash
curl -X GET "http://localhost:8000/api/customers"
```

### Example 2: Get Full Analysis for Customer

```bash
curl -X GET "http://localhost:8000/api/customers/117/analysis"
```

### Example 3: Get Paginated Links

```bash
curl -X GET "http://localhost:8000/api/customers/117/links?limit=50&offset=0"
```

### Example 4: Get Competitive Insights

```bash
curl -X GET "http://localhost:8000/api/competitive"
```

### Example 5: Compare Customer vs Industry

```bash
curl -X GET "http://localhost:8000/api/competitive/117"
```

### Example 6: Health Check

```bash
curl -X GET "http://localhost:8000/health"
```

---

## Frontend Integration

### React/TypeScript Example

```typescript
// API client configuration
const API_BASE_URL = 'http://localhost:8000';

// Fetch customer list
async function fetchCustomers() {
  const response = await fetch(`${API_BASE_URL}/api/customers`);
  const customers = await response.json();
  return customers;
}

// Fetch customer analysis
async function fetchCustomerAnalysis(customerId: number) {
  const response = await fetch(`${API_BASE_URL}/api/customers/${customerId}/analysis`);
  const data = await response.json();
  return data.data; // Extract the 'data' field
}

// Fetch dashboard data
async function fetchDashboard() {
  const response = await fetch(`${API_BASE_URL}/api/dashboard`);
  const data = await response.json();
  return data.data;
}
```

### Error Handling Example

```typescript
async function fetchWithErrorHandling(url: string) {
  try {
    const response = await fetch(url);

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'API request failed');
    }

    return await response.json();
  } catch (error) {
    console.error('API Error:', error);
    // Handle error (show notification, etc.)
    throw error;
  }
}
```

---

## Development Notes

### Running Tests

The API includes automatic validation via Pydantic models. Test endpoints using:

1. **Swagger UI**: Navigate to `http://localhost:8000/docs`
2. **ReDoc**: Navigate to `http://localhost:8000/redoc`
3. **curl**: Use examples above
4. **Postman/Insomnia**: Import the OpenAPI schema from `/openapi.json`

### Database Requirements

The API expects a SQLite database at:
```
data/output/linkops_history.db
```

Schema required:
- `customers` table (id, canonical_root, brand, created_at)
- `links_history` table (see schema.sql)

### Performance Considerations

1. **Analysis Endpoint** (`/api/customers/{id}/analysis`):
   - Runs 4 analyzers sequentially
   - Can take 1-3 seconds for large datasets
   - Consider caching for production

2. **Competitive Endpoint** (`/api/competitive`):
   - Analyzes all customers
   - Can take 2-5 seconds with many customers
   - Results are calculated on-demand

3. **Pagination**:
   - Use `limit` and `offset` for large link datasets
   - Maximum `limit` is 1000 links per request

---

## Troubleshooting

### Database Not Found Error

**Error:** `Database not found at .../linkops_history.db`

**Solution:**
1. Check that database exists: `ls data/output/linkops_history.db`
2. Initialize database using LinkDB tools
3. Verify DB_PATH in app.py matches your setup

### Import Errors

**Error:** `ModuleNotFoundError: No module named 'app.analyzers'`

**Solution:**
1. Ensure you're in the correct directory
2. Check that `app/analyzers/` exists with all analyzer files
3. Verify sys.path is set correctly in app.py

### CORS Issues

**Error:** CORS policy blocking requests from frontend

**Solution:**
1. Check `allow_origins` in CORS middleware
2. For development, `"*"` should work
3. For production, specify exact frontend URL

---

## API Versioning

Current version: **1.0.0**

Future versions may include:
- Authentication & authorization
- Rate limiting
- Caching layer
- WebSocket support for real-time updates
- Batch operations
- Export endpoints (CSV, Excel)

---

## Support & Contributing

For issues or feature requests, please contact the development team or create an issue in the project repository.

**Track 1 Backend API** - Built for LinkDB GUI Phase 1
