# TRACK 1: Backend API & Integration [1/5]

**Agent:** Backend Specialist
**Status:** Ready to Execute
**Credits:** Part of $150 budget (Claude Code)
**Estimated Time:** 2-3 hours

---

## 🎯 Mission

Du är **Track 1** i ett 5-track parallellt utvecklingsteam. Din uppgift är att bygga backend API:et som exponerar alla analyzers för frontend.

**KRITISKT:** De andra 4 tracks arbetar samtidigt. Följ dina boundaries exakt för att undvika conflicts!

---

## 🚦 Boundary Rules

### ✅ DU FÅR RÖRA:
```
gui/backend/
├── app.py                          # FastAPI main app
├── requirements.txt                # Backend dependencies
├── routes/
│   ├── __init__.py
│   ├── customers.py                # Customer endpoints
│   ├── links.py                    # Link endpoints
│   ├── competitive.py              # Benchmarking endpoints
│   └── dashboard.py                # Dashboard endpoints
├── services/
│   ├── __init__.py
│   ├── analyzer_service.py         # Wrapper för analyzers
│   ├── database_service.py         # DB queries
│   └── cache_service.py            # Optional: Redis/in-memory cache
└── models/
    ├── __init__.py
    └── response_models.py          # Pydantic models
```

### ❌ DU FÅR INTE RÖRA:
- `gui/frontend/` - Track 2, 3, 4 arbetar här
- `gui/frontend/src/components/` - Track 3 gör charts
- `gui/frontend/src/pages/` - Track 4 gör pages
- `gui/export/` - Track 5 gör export
- `../app/analyzers/` - BEFINTLIGA filer (bara importera dem)
- `../data/` - Läs-endast access

---

## 👥 Vad de Andra Tracks Gör (Rör EJ!)

| Track | Ansvar | Directory |
|-------|--------|-----------|
| **Track 2** | Frontend Core & Layout | `gui/frontend/src/components/layout/`, `App.jsx` |
| **Track 3** | Charts & Visualizations | `gui/frontend/src/components/charts/` |
| **Track 4** | Pages & Views | `gui/frontend/src/pages/` |
| **Track 5** | Utils & Export | `gui/frontend/src/utils/`, `gui/export/` |

**De förväntar sig att DU levererar fungerande API endpoints!**

---

## 📋 Din Uppgift

### Del 1: Setup (30 min)

1. **Skapa directory structure:**
   ```bash
   mkdir -p gui/backend/routes
   mkdir -p gui/backend/services
   mkdir -p gui/backend/models
   ```

2. **Skapa `gui/backend/requirements.txt`:**
   ```
   fastapi==0.104.1
   uvicorn[standard]==0.24.0
   pydantic==2.4.2
   python-multipart==0.0.6
   ```

3. **Skapa `gui/backend/app.py`:**
   - FastAPI app setup
   - CORS middleware (allow all origins för dev)
   - Include routers från routes/
   - Health check endpoint: `GET /health`

### Del 2: Database Service (30 min)

**Fil:** `gui/backend/services/database_service.py`

**Funktioner:**
```python
class DatabaseService:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def get_all_customers(self) -> List[Dict]:
        """Get all customers with basic stats."""
        # SELECT from customers + COUNT links

    def get_customer(self, customer_id: int) -> Optional[Dict]:
        """Get single customer details."""

    def get_customer_links(self, customer_id: int,
                          offset: int = 0,
                          limit: int = 50) -> List[Dict]:
        """Get links for customer (paginated)."""

    def get_all_links(self, filters: Dict,
                     offset: int = 0,
                     limit: int = 50) -> List[Dict]:
        """Get all links with filters."""
```

### Del 3: Analyzer Service (45 min)

**Fil:** `gui/backend/services/analyzer_service.py`

**Uppgift:**
- Importera alla analyzers från `../../app/analyzers/`
- Wrapper functions som kör analyzers
- Konvertera dataclasses till dicts för JSON serialization
- Error handling

**Funktioner:**
```python
class AnalyzerService:
    def __init__(self, db_path: str):
        self.db_path = db_path
        # Initialize analyzers
        self.history_analyzer = LinkHistoryAnalyzer(db_path)
        self.anchor_analyzer = AnchorQualityAnalyzer(db_path)
        # ... etc

    def get_comprehensive_analysis(self, customer_id: int) -> Dict:
        """Run all analyzers and return unified result."""
        # Kör alla analyzers
        # Convert dataclasses to dicts
        # Calculate overall score
        # Return combined result

    def get_anchor_analysis(self, customer_id: int) -> Dict:
        """Get anchor quality analysis."""

    def get_temporal_analysis(self, customer_id: int) -> Dict:
        """Get temporal patterns."""

    def get_domain_analysis(self, customer_id: int) -> Dict:
        """Get domain quality."""

    def get_competitive_insights(self) -> Dict:
        """Get industry benchmarks."""

    def get_customer_comparison(self, customer_id: int) -> Dict:
        """Compare customer vs industry."""
```

### Del 4: Response Models (30 min)

**Fil:** `gui/backend/models/response_models.py`

Skapa Pydantic models för API responses:
```python
from pydantic import BaseModel
from typing import List, Dict, Optional

class ApiResponse(BaseModel):
    success: bool
    data: Optional[Dict] = None
    error: Optional[str] = None
    meta: Optional[Dict] = None

class Customer(BaseModel):
    id: int
    canonical_root: str
    brand: str
    total_links: int
    # ... etc

class LinkAnalysis(BaseModel):
    customer_id: int
    overall_score: float
    link_history: Dict
    anchor_quality: Optional[Dict]
    # ... etc
```

### Del 5: API Routes (60 min)

#### 5.1 `gui/backend/routes/dashboard.py`
```python
from fastapi import APIRouter, HTTPException
from ..services.analyzer_service import AnalyzerService
from ..services.database_service import DatabaseService

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

@router.get("/metrics")
def get_dashboard_metrics():
    """Get overall dashboard KPIs."""
    # Total customers
    # Total links
    # Average scores
    # etc
    pass
```

#### 5.2 `gui/backend/routes/customers.py`
```python
router = APIRouter(prefix="/api/customers", tags=["customers"])

@router.get("")
def get_customers():
    """List all customers with basic stats."""
    pass

@router.get("/{customer_id}")
def get_customer(customer_id: int):
    """Get customer details."""
    pass

@router.get("/{customer_id}/analysis")
def get_customer_analysis(customer_id: int):
    """Get comprehensive analysis for customer."""
    # Detta är det viktigaste endpoint!
    # Track 4 (Pages) förväntar sig denna data!
    pass

@router.get("/{customer_id}/links")
def get_customer_links(customer_id: int, offset: int = 0, limit: int = 50):
    """Get links for customer (paginated)."""
    pass
```

#### 5.3 `gui/backend/routes/links.py`
```python
router = APIRouter(prefix="/api/links", tags=["links"])

@router.get("")
def get_links(
    customer_id: Optional[int] = None,
    anchor_type: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    offset: int = 0,
    limit: int = 50
):
    """Get all links with filters."""
    pass
```

#### 5.4 `gui/backend/routes/competitive.py`
```python
router = APIRouter(prefix="/api/competitive", tags=["competitive"])

@router.get("/overview")
def get_competitive_overview():
    """Get industry benchmarks."""
    pass

@router.get("/compare")
def compare_customer(customer_id: int):
    """Compare customer vs industry."""
    pass
```

### Del 6: Testing & Error Handling (30 min)

1. **Start server:**
   ```bash
   cd gui/backend
   uvicorn app:app --reload --port 8000
   ```

2. **Test alla endpoints:**
   - `GET http://localhost:8000/health`
   - `GET http://localhost:8000/api/customers`
   - `GET http://localhost:8000/api/customers/117/analysis`
   - Etc.

3. **Proper error handling:**
   - 404 när customer inte finns
   - 500 med informative error messages
   - Validation errors (422)

4. **Logging:**
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)
   ```

---

## 📊 Deliverables Checklist

- [ ] `gui/backend/app.py` - FastAPI app fungerar
- [ ] `gui/backend/requirements.txt` - Dependencies listade
- [ ] `gui/backend/services/database_service.py` - DB queries
- [ ] `gui/backend/services/analyzer_service.py` - Analyzer integration
- [ ] `gui/backend/models/response_models.py` - Pydantic models
- [ ] `gui/backend/routes/dashboard.py` - Dashboard endpoints
- [ ] `gui/backend/routes/customers.py` - Customer endpoints
- [ ] `gui/backend/routes/links.py` - Link endpoints
- [ ] `gui/backend/routes/competitive.py` - Competitive endpoints
- [ ] Server startar utan errors
- [ ] Alla endpoints fungerar (test med browser/Postman)
- [ ] Proper error handling
- [ ] CORS enabled för frontend

---

## 🎯 Success Criteria

1. **Server starts successfully:**
   ```bash
   uvicorn app:app --reload --port 8000
   # No errors
   ```

2. **Health check works:**
   ```bash
   curl http://localhost:8000/health
   # {"status": "healthy"}
   ```

3. **Main endpoint works:**
   ```bash
   curl http://localhost:8000/api/customers/117/analysis
   # Returns full analysis JSON
   ```

4. **Fast response times:**
   - Simple queries: <200ms
   - Complex analysis: <2s
   - Paginated lists: <500ms

5. **Proper JSON format:**
   ```json
   {
     "success": true,
     "data": { ... },
     "meta": {
       "timestamp": "2025-11-12T...",
       "execution_time_ms": 45
     }
   }
   ```

---

## 🚨 Critical Notes

### Database Path
```python
import sys
from pathlib import Path

# DB path relative to backend directory
DB_PATH = Path(__file__).parent.parent.parent / "data" / "output" / "linkops_history.db"
```

### Import Analyzers
```python
# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "app"))

from analyzers.link_history_analyzer import LinkHistoryAnalyzer
from analyzers.anchor_quality_analyzer import AnchorQualityAnalyzer
# ... etc
```

### CORS Setup
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Dataclass to Dict
```python
import dataclasses

def to_dict(obj):
    if dataclasses.is_dataclass(obj):
        return dataclasses.asdict(obj)
    return obj
```

---

## 🔄 Handoff to Other Tracks

När du är klar, skapa: `gui/backend/API_DOCUMENTATION.md`

**Innehåll:**
- Alla endpoints dokumenterade
- Request/response examples
- Base URL: `http://localhost:8000`
- How to start server

**De andra tracks behöver denna info för att anropa ditt API!**

---

## 💡 Tips & Optimization

### Optional: Caching
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def get_customer_analysis_cached(customer_id: int):
    # Cache expensive operations
    pass
```

### Optional: Background Tasks
```python
from fastapi import BackgroundTasks

@router.post("/analyze")
async def trigger_analysis(customer_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(run_analysis, customer_id)
    return {"message": "Analysis started"}
```

### Performance
- Use connection pooling för SQLite
- Lazy load analyzers
- Stream large responses

---

## 🎬 Ready to Start?

1. **Open Claude Code** (med $150 credits)
2. **Load this file:** `TRACK_1_BACKEND_API.md`
3. **Tell Claude Code:**
   ```
   Execute TRACK_1_BACKEND_API.md

   You are Track 1 of 5 parallel development tracks.
   Build the complete backend API following the specification.
   DO NOT touch frontend/ - other tracks are working there.

   Start with directory setup, then build services, then routes.
   Test each endpoint as you build it.

   When done, create API_DOCUMENTATION.md for other tracks.
   ```

4. **Let it run!** ☕

---

**Track 1 är redo att köras! Backend blir grunden för alla andra tracks.** 🚀

*Estimated completion: 2-3 hours*
*Budget: ~$20-30 of $150 credits*
