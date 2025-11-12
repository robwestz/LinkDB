from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Add parent directory to path to access the 'app' module
# The current file is in linkdb/gui/backend, so we need to go up three levels to reach linkdb/
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from app.analyzers.link_history_analyzer import LinkHistoryAnalyzer
from app.analyzers.anchor_quality_analyzer import AnchorQualityAnalyzer
from app.analyzers.temporal_pattern_analyzer import TemporalPatternAnalyzer
from app.analyzers.domain_quality_analyzer import DomainQualityAnalyzer
# The spec mentions competitive_comparison.py but the example doesn't use it. I'll import it for later.
from app.analyzers.competitive_comparison import CompetitiveComparison

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

@app.get("/api/customers/{customer_id}/analysis")
def get_customer_analysis(customer_id: int):
    """Get complete analysis for a customer."""
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
