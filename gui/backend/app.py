from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path
import sqlite3
from typing import Optional

# Add parent directory to path to access the 'app' module
# The current file is in linkdb/gui/backend, so we need to go up three levels to reach linkdb/
project_root = str(Path(__file__).parent.parent.parent)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import analyzers (with error handling for development)
try:
    from app.analyzers.link_history_analyzer import LinkHistoryAnalyzer
    from app.analyzers.anchor_quality_analyzer import AnchorQualityAnalyzer
    from app.analyzers.temporal_pattern_analyzer import TemporalPatternAnalyzer
    from app.analyzers.domain_quality_analyzer import DomainQualityAnalyzer
    from app.analyzers.competitive_comparison import CompetitiveComparison
    ANALYZERS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Analyzers not available: {e}")
    ANALYZERS_AVAILABLE = False

app = FastAPI(title="LinkDB Analytics API")

# CORS middleware to allow requests from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Define the absolute path to the database
DB_PATH = str(Path(__file__).parent.parent.parent / "data" / "output" / "linkops_history.db")

def get_db_connection():
    """Helper to get database connection."""
    return sqlite3.connect(DB_PATH)

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "LinkDB Analytics API"}

@app.get("/api/customers")
def get_customers():
    """Get all customers with basic metrics."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get all unique customers
        cursor.execute("""
            SELECT DISTINCT customer_id, canonical_root, brand
            FROM customer_history
            ORDER BY customer_id
        """)

        customers = []
        for row in cursor.fetchall():
            customer_id, canonical_root, brand = row

            # Get link count for this customer
            cursor.execute("""
                SELECT COUNT(*) FROM customer_history WHERE customer_id = ?
            """, (customer_id,))
            total_links = cursor.fetchone()[0]

            # Calculate a simple health score (can be enhanced)
            health_score = min(100, (total_links / 50) * 100)

            customers.append({
                "id": customer_id,
                "canonical_root": canonical_root,
                "brand": brand,
                "total_links": total_links,
                "health_score": round(health_score, 1)
            })

        conn.close()

        return {
            "success": True,
            "data": customers
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching customers: {str(e)}")

@app.get("/api/dashboard/metrics")
def get_dashboard_metrics():
    """Get dashboard overview metrics."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Total customers
        cursor.execute("SELECT COUNT(DISTINCT customer_id) FROM customer_history")
        total_customers = cursor.fetchone()[0]

        # Total links
        cursor.execute("SELECT COUNT(*) FROM customer_history")
        total_links = cursor.fetchone()[0]

        # Average health (simplified)
        avg_health = 75.2

        # Top performers (by link count)
        cursor.execute("""
            SELECT canonical_root, COUNT(*) as link_count
            FROM customer_history
            GROUP BY customer_id, canonical_root
            ORDER BY link_count DESC
            LIMIT 10
        """)
        top_performers = [{"domain": row[0], "links": row[1]} for row in cursor.fetchall()]

        conn.close()

        return {
            "success": True,
            "data": {
                "total_customers": total_customers,
                "total_links": total_links,
                "avg_health": avg_health,
                "top_performers": top_performers
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching dashboard metrics: {str(e)}")

@app.get("/api/competitive/overview")
def get_competitive_overview():
    """Get competitive benchmarking overview."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Total customers
        cursor.execute("SELECT COUNT(DISTINCT customer_id) FROM customer_history")
        total_customers = cursor.fetchone()[0]

        # Average links per customer
        cursor.execute("""
            SELECT AVG(link_count) FROM (
                SELECT COUNT(*) as link_count
                FROM customer_history
                GROUP BY customer_id
            )
        """)
        avg_total_links = cursor.fetchone()[0] or 0

        # Median links
        cursor.execute("""
            SELECT COUNT(*) as link_count
            FROM customer_history
            GROUP BY customer_id
            ORDER BY link_count
        """)
        link_counts = [row[0] for row in cursor.fetchall()]
        median_total_links = link_counts[len(link_counts)//2] if link_counts else 0

        # Top 10 by volume
        cursor.execute("""
            SELECT canonical_root, COUNT(*) as link_count
            FROM customer_history
            GROUP BY customer_id, canonical_root
            ORDER BY link_count DESC
            LIMIT 10
        """)
        top_10_by_volume = [[row[0], row[1]] for row in cursor.fetchall()]

        conn.close()

        return {
            "success": True,
            "data": {
                "total_customers": total_customers,
                "avg_total_links": avg_total_links,
                "median_total_links": median_total_links,
                "avg_quality": 75.0,
                "top_10_by_volume": top_10_by_volume,
                "top_10_by_quality": top_10_by_volume[:10],  # Simplified
                "customers": []
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching competitive overview: {str(e)}")

@app.get("/api/links")
def get_links(
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    search: Optional[str] = None,
    customer_id: Optional[int] = None,
    anchor_type: Optional[str] = None
):
    """Get links with pagination and filtering."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Build query
        query = "SELECT customer_id, canonical_root, pub_domain, target_url, anchor_text, published_at FROM customer_history WHERE 1=1"
        params = []

        if search:
            query += " AND (canonical_root LIKE ? OR pub_domain LIKE ? OR anchor_text LIKE ?)"
            search_pattern = f"%{search}%"
            params.extend([search_pattern, search_pattern, search_pattern])

        if customer_id:
            query += " AND customer_id = ?"
            params.append(customer_id)

        query += f" LIMIT {limit} OFFSET {offset}"

        cursor.execute(query, params)

        links = []
        for row in cursor.fetchall():
            links.append({
                "customer_id": row[0],
                "customer": row[1],
                "pub_domain": row[2],
                "target_url": row[3],
                "anchor_text": row[4],
                "published_at": row[5],
                "anchor_type": "exact"  # Simplified
            })

        conn.close()

        return {
            "success": True,
            "data": links
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching links: {str(e)}")

@app.get("/api/customers/{customer_id}/analysis")
def get_customer_analysis(customer_id: int):
    """Get complete analysis for a customer."""
    if not ANALYZERS_AVAILABLE:
        raise HTTPException(status_code=503, detail="Analysis modules not available")

    try:
        # Initialize analyzers with the database path
        history_analyzer = LinkHistoryAnalyzer(DB_PATH)
        anchor_analyzer = AnchorQualityAnalyzer(DB_PATH)
        temporal_analyzer = TemporalPatternAnalyzer(DB_PATH)
        domain_analyzer = DomainQualityAnalyzer(DB_PATH)

        # Run analysis
        history = history_analyzer.analyze_customer(customer_id)
        anchor = anchor_analyzer.analyze_customer(customer_id)
        temporal = temporal_analyzer.analyze_customer(customer_id)
        domain = domain_analyzer.analyze_customer(customer_id)

        if not history:
            raise HTTPException(status_code=404, detail=f"Customer with ID {customer_id} not found")

        # Calculate overall score from available analyzer scores
        scores = []
        if anchor and hasattr(anchor, 'quality_score'):
            scores.append(anchor.quality_score)
        if temporal and hasattr(temporal, 'health_score'):
            scores.append(temporal.health_score)
        if domain and hasattr(domain, 'quality_score'):
            scores.append(domain.quality_score)

        overall_score = sum(scores) / len(scores) if scores else 0

        # Build the response structure as defined in the spec
        return {
            "success": True,
            "data": {
                "customer_id": customer_id,
                "canonical_root": history.canonical_root,
                "brand": history.brand,
                "overall_score": round(overall_score, 1),
                "link_history": {
                    "total_links": history.total_links,
                    "unique_pub_domains": history.unique_pub_domains,
                    "unique_target_urls": history.unique_target_urls,
                    "links_per_month": round(history.links_per_month, 1),
                    "primary_strategy": history.primary_strategy,
                    "recommendations": history.recommendations,
                    "most_common_anchors": history.most_common_anchors,
                    "most_linked_urls": history.most_linked_urls
                },
                "anchor_quality": {
                    "quality_score": round(anchor.quality_score, 1),
                    "diversity_score": round(anchor.diversity_score, 1),
                    "over_optimization_risk": anchor.over_optimization_risk,
                    "shannon_entropy": round(anchor.shannon_entropy, 2),
                    "exact_match_ratio": round(anchor.exact_match_ratio * 100, 1),
                    "branded_ratio": round(anchor.branded_ratio * 100, 1),
                    "commercial_keywords_ratio": round(anchor.commercial_keywords_ratio * 100, 1),
                    "warnings": anchor.warnings,
                    "top_anchors": anchor.top_anchors
                } if anchor else None,
                "temporal_patterns": {
                    "health_score": round(temporal.health_score, 1),
                    "links_per_month": round(temporal.links_per_month, 1),
                    "velocity_trend": temporal.velocity_trend,
                    "consistency_score": round(temporal.consistency_score, 1),
                    "monthly_distribution": temporal.monthly_distribution,
                    "has_unnatural_spikes": temporal.has_unnatural_spikes,
                    "warnings": temporal.warnings,
                    "insights": temporal.insights
                } if temporal else None,
                "domain_quality": {
                    "quality_score": round(domain.quality_score, 1),
                    "unique_domains": domain.unique_domains,
                    "diversity_score": round(domain.domain_diversity_score, 1),
                    "cross_linking_score": round(domain.cross_linking_score, 1),
                    "top_tlds": domain.top_tlds,
                    "geographic_diversity": domain.geographic_diversity,
                    "warnings": domain.warnings,
                    "top_domains": domain.top_domains
                } if domain else None
            }
        }
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail=f"Database not found at {DB_PATH}. Please ensure the path is correct.")
    except Exception as e:
        # Return a detailed error message for debugging
        return HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # Run the server on host 0.0.0.0 to make it accessible from the frontend container/machine
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
