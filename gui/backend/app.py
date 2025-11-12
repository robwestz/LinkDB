"""
LinkDB Backend API - FastAPI REST API for LinkDB Analytics

This API exposes all analyzers and provides comprehensive link analysis endpoints.
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any
import sys
from pathlib import Path
import sqlite3
from dataclasses import asdict

# Add parent directory to path to access the 'app' module
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.analyzers.link_history_analyzer import LinkHistoryAnalyzer
from app.analyzers.anchor_quality_analyzer import AnchorQualityAnalyzer
from app.analyzers.temporal_pattern_analyzer import TemporalPatternAnalyzer
from app.analyzers.domain_quality_analyzer import DomainQualityAnalyzer
from app.analyzers.competitive_comparison import CompetitiveComparison

# Initialize FastAPI app
app = FastAPI(
    title="LinkDB Analytics API",
    description="REST API for LinkDB link analysis and planning system",
    version="1.0.0"
)

# CORS middleware - allows requests from frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database path
DB_PATH = str(Path(__file__).parent.parent.parent / "data" / "output" / "linkops_history.db")


# ============================================================================
# PYDANTIC MODELS - Request/Response validation
# ============================================================================

class CustomerBasic(BaseModel):
    """Basic customer information"""
    id: int
    canonical_root: str
    brand: Optional[str]
    total_links: int


class CustomerDetail(BaseModel):
    """Detailed customer information"""
    id: int
    canonical_root: str
    brand: Optional[str]
    created_at: Optional[str]
    total_links: int
    unique_pub_domains: int
    unique_target_urls: int
    links_per_month: float


class LinkRecord(BaseModel):
    """Individual link record"""
    id: int
    pub_page_url: str
    pub_domain: Optional[str]
    target_url: str
    target_domain: Optional[str]
    anchor_text: Optional[str]
    anchor_type: Optional[str]
    link_type: Optional[str]
    language: Optional[str]
    published_at: Optional[str]
    topic_tags: Optional[str]
    created_at: Optional[str]


class MonthlyLinkGroup(BaseModel):
    """Links grouped by month"""
    year: int
    month: int
    month_name: str
    period: str
    link_count: int
    unique_pub_domains: int
    unique_target_urls: int
    top_anchors: List[tuple]


class AnalysisResponse(BaseModel):
    """Complete analysis response"""
    success: bool
    data: Dict[str, Any]


class ErrorResponse(BaseModel):
    """Error response"""
    success: bool = False
    error: str
    detail: Optional[str] = None


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_db_connection():
    """Get database connection with error handling"""
    if not Path(DB_PATH).exists():
        raise HTTPException(
            status_code=500,
            detail=f"Database not found at {DB_PATH}. Please initialize the database first."
        )
    try:
        con = sqlite3.connect(DB_PATH)
        con.row_factory = sqlite3.Row
        return con
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")


def safe_round(value, decimals=1):
    """Safely round a value, handling None"""
    if value is None:
        return None
    try:
        return round(float(value), decimals)
    except (ValueError, TypeError):
        return value


# ============================================================================
# API ROUTES - CUSTOMERS
# ============================================================================

@app.get("/api/customers", response_model=List[CustomerBasic])
async def list_customers():
    """
    List all customers with basic information.

    Returns a list of all customers with their ID, canonical root, brand, and total links.
    """
    con = get_db_connection()
    try:
        customers = con.execute("""
            SELECT
                c.id,
                c.canonical_root,
                c.brand,
                COUNT(l.id) as total_links
            FROM customers c
            LEFT JOIN links_history l ON c.id = l.customer_id
            GROUP BY c.id
            ORDER BY total_links DESC, c.canonical_root
        """).fetchall()

        return [
            {
                "id": c['id'],
                "canonical_root": c['canonical_root'],
                "brand": c['brand'],
                "total_links": c['total_links']
            }
            for c in customers
        ]
    finally:
        con.close()


@app.get("/api/customers/{customer_id}", response_model=CustomerDetail)
async def get_customer(customer_id: int):
    """
    Get detailed information for a specific customer.

    Args:
        customer_id: Customer ID

    Returns:
        Detailed customer information including link statistics
    """
    con = get_db_connection()
    try:
        customer = con.execute("""
            SELECT
                c.id,
                c.canonical_root,
                c.brand,
                c.created_at,
                COUNT(l.id) as total_links,
                COUNT(DISTINCT l.pub_domain) as unique_pub_domains,
                COUNT(DISTINCT l.target_url) as unique_target_urls
            FROM customers c
            LEFT JOIN links_history l ON c.id = l.customer_id
            WHERE c.id = ?
            GROUP BY c.id
        """, (customer_id,)).fetchone()

        if not customer:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")

        # Calculate links per month (rough estimate based on 6 months)
        links_per_month = customer['total_links'] / 6 if customer['total_links'] > 0 else 0

        return {
            "id": customer['id'],
            "canonical_root": customer['canonical_root'],
            "brand": customer['brand'],
            "created_at": customer['created_at'],
            "total_links": customer['total_links'],
            "unique_pub_domains": customer['unique_pub_domains'],
            "unique_target_urls": customer['unique_target_urls'],
            "links_per_month": safe_round(links_per_month, 1)
        }
    finally:
        con.close()


@app.get("/api/customers/{customer_id}/analysis")
async def get_customer_analysis(customer_id: int):
    """
    Get complete analysis for a customer.

    Runs all analyzers and returns comprehensive analysis including:
    - Link history analysis
    - Anchor quality analysis
    - Temporal pattern analysis
    - Domain quality analysis

    Args:
        customer_id: Customer ID

    Returns:
        Complete analysis data with overall score
    """
    try:
        # Initialize all analyzers
        history_analyzer = LinkHistoryAnalyzer(DB_PATH)
        anchor_analyzer = AnchorQualityAnalyzer(DB_PATH)
        temporal_analyzer = TemporalPatternAnalyzer(DB_PATH)
        domain_analyzer = DomainQualityAnalyzer(DB_PATH)

        # Run all analyses
        history = history_analyzer.analyze_customer(customer_id)
        anchor = anchor_analyzer.analyze_customer(customer_id)
        temporal = temporal_analyzer.analyze_customer(customer_id)
        domain = domain_analyzer.analyze_customer(customer_id)

        if not history:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found or has no data")

        # Calculate overall score from available analyzer scores
        scores = []
        if anchor and hasattr(anchor, 'quality_score'):
            scores.append(anchor.quality_score)
        if temporal and hasattr(temporal, 'health_score'):
            scores.append(temporal.health_score)
        if domain and hasattr(domain, 'quality_score'):
            scores.append(domain.quality_score)

        overall_score = sum(scores) / len(scores) if scores else 0

        # Build comprehensive response
        return {
            "success": True,
            "data": {
                "customer_id": customer_id,
                "canonical_root": history.canonical_root,
                "brand": history.brand,
                "overall_score": safe_round(overall_score, 1),
                "link_history": {
                    "total_links": history.total_links,
                    "unique_pub_domains": history.unique_pub_domains,
                    "unique_target_urls": history.unique_target_urls,
                    "links_per_month": safe_round(history.links_per_month, 1),
                    "primary_strategy": history.primary_strategy,
                    "recommendations": history.recommendations,
                    "most_common_anchors": history.most_common_anchors[:10],
                    "most_linked_urls": history.most_linked_urls[:10]
                },
                "anchor_quality": {
                    "quality_score": safe_round(anchor.quality_score, 1),
                    "diversity_score": safe_round(anchor.diversity_score, 1),
                    "over_optimization_risk": anchor.over_optimization_risk,
                    "shannon_entropy": safe_round(anchor.shannon_entropy, 2),
                    "exact_match_ratio": safe_round(anchor.exact_match_ratio * 100, 1),
                    "branded_ratio": safe_round(anchor.branded_ratio * 100, 1),
                    "commercial_keywords_ratio": safe_round(anchor.commercial_keywords_ratio * 100, 1),
                    "warnings": anchor.warnings,
                    "top_anchors": anchor.top_anchors[:15]
                } if anchor else None,
                "temporal_patterns": {
                    "health_score": safe_round(temporal.health_score, 1),
                    "links_per_month": safe_round(temporal.links_per_month, 1),
                    "velocity_trend": temporal.velocity_trend,
                    "consistency_score": safe_round(temporal.consistency_score, 1),
                    "monthly_distribution": temporal.monthly_distribution,
                    "has_unnatural_spikes": temporal.has_unnatural_spikes,
                    "warnings": temporal.warnings,
                    "insights": temporal.insights
                } if temporal else None,
                "domain_quality": {
                    "quality_score": safe_round(domain.quality_score, 1),
                    "unique_domains": domain.unique_domains,
                    "diversity_score": safe_round(domain.domain_diversity_score, 1),
                    "cross_linking_score": safe_round(domain.cross_linking_score, 1),
                    "top_tlds": domain.top_tlds[:10],
                    "geographic_diversity": domain.geographic_diversity,
                    "warnings": domain.warnings,
                    "insights": domain.insights,
                    "top_domains": domain.top_domains[:15]
                } if domain else None
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")


@app.get("/api/customers/{customer_id}/links")
async def get_customer_links(
    customer_id: int,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    Get link history for a customer with pagination.

    Args:
        customer_id: Customer ID
        limit: Maximum number of links to return (1-1000, default 100)
        offset: Number of links to skip (default 0)

    Returns:
        Paginated list of links
    """
    con = get_db_connection()
    try:
        # Check if customer exists
        customer = con.execute("SELECT id FROM customers WHERE id = ?", (customer_id,)).fetchone()
        if not customer:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")

        # Get total count
        total = con.execute(
            "SELECT COUNT(*) as count FROM links_history WHERE customer_id = ?",
            (customer_id,)
        ).fetchone()['count']

        # Get links with pagination
        links = con.execute("""
            SELECT *
            FROM links_history
            WHERE customer_id = ?
            ORDER BY published_at DESC, created_at DESC
            LIMIT ? OFFSET ?
        """, (customer_id, limit, offset)).fetchall()

        return {
            "success": True,
            "data": {
                "total": total,
                "limit": limit,
                "offset": offset,
                "links": [dict(link) for link in links]
            }
        }
    finally:
        con.close()


@app.get("/api/customers/{customer_id}/links/monthly")
async def get_customer_links_monthly(customer_id: int):
    """
    Get links grouped by publication month.

    Args:
        customer_id: Customer ID

    Returns:
        Links grouped by month with aggregated statistics
    """
    con = get_db_connection()
    try:
        # Check if customer exists
        customer = con.execute("SELECT id FROM customers WHERE id = ?", (customer_id,)).fetchone()
        if not customer:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")

        # Get links grouped by month
        monthly_data = con.execute("""
            SELECT
                strftime('%Y', COALESCE(published_at, created_at)) as year,
                strftime('%m', COALESCE(published_at, created_at)) as month,
                COUNT(*) as link_count,
                COUNT(DISTINCT pub_domain) as unique_pub_domains,
                COUNT(DISTINCT target_url) as unique_target_urls,
                GROUP_CONCAT(DISTINCT anchor_text) as anchors
            FROM links_history
            WHERE customer_id = ?
                AND COALESCE(published_at, created_at) IS NOT NULL
            GROUP BY year, month
            ORDER BY year DESC, month DESC
        """, (customer_id,)).fetchall()

        # Format response
        months = []
        month_names = {
            "01": "January", "02": "February", "03": "March", "04": "April",
            "05": "May", "06": "June", "07": "July", "08": "August",
            "09": "September", "10": "October", "11": "November", "12": "December"
        }

        for row in monthly_data:
            month_name = month_names.get(row['month'], "Unknown")
            months.append({
                "year": int(row['year']),
                "month": int(row['month']),
                "month_name": month_name,
                "period": f"{row['year']}-{row['month']}",
                "link_count": row['link_count'],
                "unique_pub_domains": row['unique_pub_domains'],
                "unique_target_urls": row['unique_target_urls']
            })

        return {
            "success": True,
            "data": {
                "customer_id": customer_id,
                "total_months": len(months),
                "months": months
            }
        }
    finally:
        con.close()


# ============================================================================
# API ROUTES - COMPETITIVE ANALYSIS
# ============================================================================

@app.get("/api/competitive")
async def get_competitive_insights():
    """
    Get industry-wide competitive insights.

    Analyzes all customers and provides:
    - Industry benchmarks
    - Top performers by volume and quality
    - Distribution analysis

    Returns:
        Competitive insights across all customers
    """
    try:
        comp = CompetitiveComparison(DB_PATH)
        insights = comp.analyze_all_customers()

        if not insights:
            raise HTTPException(status_code=404, detail="No customer data found for analysis")

        return {
            "success": True,
            "data": {
                "total_customers_analyzed": insights.total_customers_analyzed,
                "benchmarks": {
                    "avg_total_links": safe_round(insights.avg_total_links, 1),
                    "median_total_links": safe_round(insights.median_total_links, 0),
                    "avg_links_per_month": safe_round(insights.avg_links_per_month, 1),
                    "avg_anchor_diversity": safe_round(insights.avg_anchor_diversity, 1),
                    "avg_domain_diversity": safe_round(insights.avg_domain_diversity, 1)
                },
                "top_performers": {
                    "by_volume": insights.top_10_by_volume,
                    "by_quality": [(d, safe_round(s, 1)) for d, s in insights.top_10_by_quality],
                    "by_diversity": [(d, safe_round(s, 1)) for d, s in insights.top_10_by_diversity]
                },
                "distribution": {
                    "volume": insights.volume_distribution,
                    "quality_tiers": insights.quality_tiers
                }
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Competitive analysis error: {str(e)}")


@app.get("/api/competitive/{customer_id}")
async def compare_customer(customer_id: int):
    """
    Compare a specific customer against industry benchmarks.

    Args:
        customer_id: Customer ID

    Returns:
        Customer comparison with industry benchmarks and percentile rankings
    """
    try:
        comp = CompetitiveComparison(DB_PATH)
        comparison = comp.compare_customer(customer_id)

        if not comparison:
            raise HTTPException(status_code=404, detail=f"Customer {customer_id} not found")

        # Also get industry insights for context
        insights = comparison.get('insights')

        return {
            "success": True,
            "data": {
                "customer": comparison['customer'],
                "metrics": {
                    "total_links": comparison['total_links'],
                    "unique_domains": comparison['unique_domains'],
                    "anchor_diversity": safe_round(comparison['anchor_diversity'], 1),
                    "domain_diversity": safe_round(comparison['domain_diversity'], 1)
                },
                "vs_industry": {
                    "volume_percentile": safe_round(comparison['volume_percentile'], 0),
                    "quality_percentile": safe_round(comparison['quality_percentile'], 0),
                    "vs_avg_links": safe_round(comparison['vs_avg_links'], 1),
                    "vs_median_links": safe_round(comparison['vs_median_links'], 0)
                },
                "industry_context": {
                    "avg_total_links": safe_round(insights.avg_total_links, 1) if insights else None,
                    "median_total_links": safe_round(insights.median_total_links, 0) if insights else None
                }
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison error: {str(e)}")


# ============================================================================
# API ROUTES - DASHBOARD
# ============================================================================

@app.get("/api/dashboard")
async def get_dashboard_data():
    """
    Get dashboard overview data.

    Provides a comprehensive overview including:
    - Total customers and links
    - Recent activity
    - Top customers by link volume
    - System health metrics

    Returns:
        Dashboard overview data
    """
    con = get_db_connection()
    try:
        # Overall statistics
        stats = con.execute("""
            SELECT
                COUNT(DISTINCT c.id) as total_customers,
                COUNT(l.id) as total_links,
                COUNT(DISTINCT l.pub_domain) as total_pub_domains,
                COUNT(DISTINCT l.target_url) as total_target_urls
            FROM customers c
            LEFT JOIN links_history l ON c.id = l.customer_id
        """).fetchone()

        # Top customers by volume
        top_customers = con.execute("""
            SELECT
                c.id,
                c.canonical_root,
                c.brand,
                COUNT(l.id) as total_links
            FROM customers c
            LEFT JOIN links_history l ON c.id = l.customer_id
            GROUP BY c.id
            ORDER BY total_links DESC
            LIMIT 10
        """).fetchall()

        # Recent links (last 30 days equivalent)
        recent_links = con.execute("""
            SELECT COUNT(*) as count
            FROM links_history
            WHERE created_at >= datetime('now', '-30 days')
        """).fetchone()

        # Activity by month (last 6 months)
        monthly_activity = con.execute("""
            SELECT
                strftime('%Y-%m', COALESCE(published_at, created_at)) as month,
                COUNT(*) as link_count
            FROM links_history
            WHERE COALESCE(published_at, created_at) >= date('now', '-6 months')
            GROUP BY month
            ORDER BY month DESC
        """).fetchall()

        return {
            "success": True,
            "data": {
                "overview": {
                    "total_customers": stats['total_customers'],
                    "total_links": stats['total_links'],
                    "total_pub_domains": stats['total_pub_domains'],
                    "total_target_urls": stats['total_target_urls'],
                    "recent_links_30d": recent_links['count'] if recent_links else 0
                },
                "top_customers": [
                    {
                        "id": c['id'],
                        "canonical_root": c['canonical_root'],
                        "brand": c['brand'],
                        "total_links": c['total_links']
                    }
                    for c in top_customers
                ],
                "monthly_activity": [
                    {"month": m['month'], "link_count": m['link_count']}
                    for m in monthly_activity
                ]
            }
        }
    finally:
        con.close()


# ============================================================================
# HEALTH & INFO ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """API root - basic info"""
    return {
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


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_exists = Path(DB_PATH).exists()

    return {
        "status": "healthy" if db_exists else "degraded",
        "database": {
            "path": DB_PATH,
            "exists": db_exists
        },
        "api_version": "1.0.0"
    }


# ============================================================================
# RUN SERVER
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    print("=" * 70)
    print("🚀 Starting LinkDB Backend API")
    print("=" * 70)
    print(f"📊 Database: {DB_PATH}")
    print(f"🌐 Server: http://localhost:8000")
    print(f"📚 API Docs: http://localhost:8000/docs")
    print("=" * 70)
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
