# LinkDB Backend API

FastAPI-based REST API for LinkDB Analytics System (Track 1 - Phase 1)

## Quick Start

### Installation

```bash
cd gui/backend
pip install -r requirements.txt
```

### Run Server

```bash
python app.py
```

Or using uvicorn:
```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Server will start on: **http://localhost:8000**

## API Documentation

- **Interactive Docs (Swagger):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc
- **Full Documentation:** See [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)

## Available Endpoints

### Health & Info
- `GET /` - API info
- `GET /health` - Health check

### Customers
- `GET /api/customers` - List all customers
- `GET /api/customers/{id}` - Get customer details
- `GET /api/customers/{id}/analysis` - Full customer analysis
- `GET /api/customers/{id}/links` - Get customer links (paginated)
- `GET /api/customers/{id}/links/monthly` - Monthly grouped links

### Competitive Analysis
- `GET /api/competitive` - Industry insights
- `GET /api/competitive/{id}` - Compare customer vs industry

### Dashboard
- `GET /api/dashboard` - Dashboard overview data

## Features

- **Complete Analyzer Integration**: All LinkDB analyzers exposed via REST API
  - Link History Analyzer
  - Anchor Quality Analyzer
  - Temporal Pattern Analyzer
  - Domain Quality Analyzer
  - Competitive Comparison

- **Comprehensive Error Handling**: Proper HTTP status codes and error messages

- **CORS Enabled**: Ready for frontend integration

- **Pagination Support**: Efficient data retrieval for large datasets

- **Pydantic Validation**: Request/response validation and type safety

- **Auto-generated Docs**: FastAPI automatic OpenAPI documentation

## Architecture

```
gui/backend/
├── app.py                    # Main FastAPI application
├── requirements.txt          # Python dependencies
├── API_DOCUMENTATION.md      # Complete API reference
└── README.md                 # This file

Integrates with:
../../app/analyzers/          # Core analyzer modules
  ├── link_history_analyzer.py
  ├── anchor_quality_analyzer.py
  ├── temporal_pattern_analyzer.py
  ├── domain_quality_analyzer.py
  └── competitive_comparison.py
```

## Database

**Required:** SQLite database at `../../data/output/linkops_history.db`

Initialize using LinkDB tools:
```bash
cd ../..
python init_planning_system.py
```

## Development

### Test API with curl

```bash
# Health check
curl http://localhost:8000/health

# List customers
curl http://localhost:8000/api/customers

# Get customer analysis
curl http://localhost:8000/api/customers/117/analysis

# Get dashboard
curl http://localhost:8000/api/dashboard
```

### Frontend Integration

The API is designed for integration with Track 2-5 (React frontend):

```typescript
const API_URL = 'http://localhost:8000';

// Fetch customers
const response = await fetch(`${API_URL}/api/customers`);
const customers = await response.json();
```

## Technology Stack

- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation
- **SQLite3** - Database (via Python standard library)

## Notes for Other Tracks

### Track 2, 3, 4, 5 (Frontend)

This backend provides all necessary endpoints for:
- Customer listing and selection
- Link analysis visualization
- Competitive insights
- Dashboard metrics

**DO NOT MODIFY:**
- `app.py` (unless adding new endpoints)
- `../../app/analyzers/*` (existing analyzer files)

**INTEGRATE WITH:**
- Use endpoints as documented in API_DOCUMENTATION.md
- All responses include `success` boolean for error handling
- Pagination available for large datasets

## Track 1 Deliverables ✅

- [x] Complete FastAPI backend
- [x] All analyzer integrations
- [x] Customer routes (list, details, analysis, links)
- [x] Competitive analysis routes
- [x] Dashboard route
- [x] Error handling & CORS
- [x] Pydantic models
- [x] API documentation
- [x] Health check endpoint
- [x] Pagination support

## Next Steps (Future Enhancements)

- [ ] Authentication & authorization
- [ ] Caching layer for performance
- [ ] Rate limiting
- [ ] WebSocket support for real-time updates
- [ ] Export endpoints (CSV, Excel)
- [ ] Batch operations
- [ ] Query filtering and sorting
- [ ] API versioning

---

**Track 1 Backend API** - Phase 1 Complete
Built for LinkDB GUI by Track 1 Development Team
