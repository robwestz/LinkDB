"""
Advanced Analysis Routes - Extended features for LinkDB GUI

This module provides enhanced analysis endpoints including:
- Date range filtering
- Anchor text frequency analysis
- Word frequency in anchor texts
- Target URL analysis
- Link health metrics
- Comparison analysis
"""

import re
import sqlite3
from collections import Counter
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="/api/advanced", tags=["advanced-analysis"])

# Database path
DB_PATH = str(
    Path(__file__).parent.parent.parent.parent
    / "data"
    / "output"
    / "linkops_history.db"
)


def get_db_connection():
    """Helper to get database connection."""
    return sqlite3.connect(DB_PATH)


def parse_date(date_str: Optional[str]) -> Optional[str]:
    """Parse date string in format YYYY-MM to YYYY-MM-01."""
    if not date_str:
        return None
    try:
        # Validate format YYYY-MM
        parts = date_str.split("-")
        if len(parts) != 2:
            return None
        year, month = int(parts[0]), int(parts[1])
        if year < 1900 or year > 2100 or month < 1 or month > 12:
            return None
        return f"{year:04d}-{month:02d}-01"
    except (ValueError, IndexError):
        return None


@router.get("/customers/{customer_id}/anchor-frequency")
def get_anchor_frequency(
    customer_id: int,
    from_date: Optional[str] = Query(None, description="Start date (YYYY-MM)"),
    to_date: Optional[str] = Query(None, description="End date (YYYY-MM)"),
    limit: int = Query(100, ge=1, le=500),
):
    """
    Get frequency of each anchor text used for a customer.

    Returns list of anchor texts with usage count, sorted by frequency.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Build query with date filtering
        query = """
            SELECT anchor_text, COUNT(*) as frequency
            FROM customer_history
            WHERE customer_id = ?
        """
        params = [customer_id]

        # Add date filters
        from_date_parsed = parse_date(from_date)
        to_date_parsed = parse_date(to_date)

        if from_date_parsed:
            query += " AND published_at >= ?"
            params.append(from_date_parsed)

        if to_date_parsed:
            # Add one month to include the entire end month
            year, month = map(int, to_date_parsed.split("-")[:2])
            if month == 12:
                end_date = f"{year + 1:04d}-01-01"
            else:
                end_date = f"{year:04d}-{month + 1:02d}-01"
            query += " AND published_at < ?"
            params.append(end_date)

        query += """
            GROUP BY anchor_text
            ORDER BY frequency DESC
            LIMIT ?
        """
        params.append(limit)

        cursor.execute(query, params)

        results = [
            {"anchor_text": row[0], "frequency": row[1]} for row in cursor.fetchall()
        ]

        # Calculate statistics
        total_links = sum(r["frequency"] for r in results)
        unique_anchors = len(results)

        conn.close()

        return {
            "success": True,
            "data": {
                "anchors": results,
                "statistics": {
                    "total_links": total_links,
                    "unique_anchors": unique_anchors,
                    "date_range": {"from": from_date, "to": to_date},
                },
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching anchor frequency: {str(e)}"
        )


@router.get("/customers/{customer_id}/word-frequency")
def get_word_frequency(
    customer_id: int,
    from_date: Optional[str] = Query(None, description="Start date (YYYY-MM)"),
    to_date: Optional[str] = Query(None, description="End date (YYYY-MM)"),
    min_length: int = Query(3, ge=1, description="Minimum word length"),
    limit: int = Query(100, ge=1, le=500),
):
    """
    Get frequency of individual words used in anchor texts.

    Breaks down anchor texts into words and counts each word's usage.
    Useful for identifying over-used terms and keyword patterns.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Build query
        query = """
            SELECT anchor_text
            FROM customer_history
            WHERE customer_id = ?
        """
        params = [customer_id]

        # Add date filters
        from_date_parsed = parse_date(from_date)
        to_date_parsed = parse_date(to_date)

        if from_date_parsed:
            query += " AND published_at >= ?"
            params.append(from_date_parsed)

        if to_date_parsed:
            year, month = map(int, to_date_parsed.split("-")[:2])
            if month == 12:
                end_date = f"{year + 1:04d}-01-01"
            else:
                end_date = f"{year:04d}-{month + 1:02d}-01"
            query += " AND published_at < ?"
            params.append(end_date)

        cursor.execute(query, params)

        # Count words
        word_counter = Counter()
        total_anchor_texts = 0

        for row in cursor.fetchall():
            anchor_text = row[0] or ""
            total_anchor_texts += 1

            # Extract words (alphanumeric sequences)
            words = re.findall(r"\b[a-zA-Z0-9]+\b", anchor_text.lower())

            # Filter by minimum length
            words = [w for w in words if len(w) >= min_length]

            word_counter.update(words)

        # Get top words
        top_words = [
            {
                "word": word,
                "frequency": count,
                "percentage": (
                    round((count / total_anchor_texts * 100), 2)
                    if total_anchor_texts > 0
                    else 0
                ),
            }
            for word, count in word_counter.most_common(limit)
        ]

        conn.close()

        return {
            "success": True,
            "data": {
                "words": top_words,
                "statistics": {
                    "total_anchor_texts": total_anchor_texts,
                    "unique_words": len(word_counter),
                    "top_words_shown": len(top_words),
                    "date_range": {"from": from_date, "to": to_date},
                },
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error fetching word frequency: {str(e)}"
        )


@router.get("/customers/{customer_id}/anchor-search")
def search_anchor_texts(
    customer_id: int,
    search_term: str = Query(
        ..., min_length=1, description="Word or phrase to search for"
    ),
    from_date: Optional[str] = Query(None, description="Start date (YYYY-MM)"),
    to_date: Optional[str] = Query(None, description="End date (YYYY-MM)"),
    case_sensitive: bool = Query(False, description="Case sensitive search"),
):
    """
    Search for specific word or phrase in anchor texts.

    Returns all anchor texts containing the search term with context.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Build query
        query = """
            SELECT anchor_text, pub_domain, target_url, published_at
            FROM customer_history
            WHERE customer_id = ?
        """
        params = [customer_id]

        # Add date filters
        from_date_parsed = parse_date(from_date)
        to_date_parsed = parse_date(to_date)

        if from_date_parsed:
            query += " AND published_at >= ?"
            params.append(from_date_parsed)

        if to_date_parsed:
            year, month = map(int, to_date_parsed.split("-")[:2])
            if month == 12:
                end_date = f"{year + 1:04d}-01-01"
            else:
                end_date = f"{year:04d}-{month + 1:02d}-01"
            query += " AND published_at < ?"
            params.append(end_date)

        cursor.execute(query, params)

        # Filter results by search term
        matches = []
        for row in cursor.fetchall():
            anchor_text, pub_domain, target_url, published_at = row
            anchor_text = anchor_text or ""

            # Check if search term is in anchor text
            if case_sensitive:
                if search_term in anchor_text:
                    matches.append(
                        {
                            "anchor_text": anchor_text,
                            "pub_domain": pub_domain,
                            "target_url": target_url,
                            "published_at": published_at,
                        }
                    )
            else:
                if search_term.lower() in anchor_text.lower():
                    matches.append(
                        {
                            "anchor_text": anchor_text,
                            "pub_domain": pub_domain,
                            "target_url": target_url,
                            "published_at": published_at,
                        }
                    )

        conn.close()

        return {
            "success": True,
            "data": {
                "matches": matches,
                "statistics": {
                    "total_matches": len(matches),
                    "search_term": search_term,
                    "case_sensitive": case_sensitive,
                    "date_range": {"from": from_date, "to": to_date},
                },
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error searching anchor texts: {str(e)}"
        )


@router.get("/customers/{customer_id}/target-url-analysis")
def get_target_url_analysis(
    customer_id: int,
    from_date: Optional[str] = Query(None, description="Start date (YYYY-MM)"),
    to_date: Optional[str] = Query(None, description="End date (YYYY-MM)"),
    limit: int = Query(50, ge=1, le=200),
):
    """
    Analyze target URLs - which pages receive the most links.

    Shows URL distribution, deep linking vs homepage linking.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Build query
        query = """
            SELECT target_url, COUNT(*) as link_count
            FROM customer_history
            WHERE customer_id = ?
        """
        params = [customer_id]

        # Add date filters
        from_date_parsed = parse_date(from_date)
        to_date_parsed = parse_date(to_date)

        if from_date_parsed:
            query += " AND published_at >= ?"
            params.append(from_date_parsed)

        if to_date_parsed:
            year, month = map(int, to_date_parsed.split("-")[:2])
            if month == 12:
                end_date = f"{year + 1:04d}-01-01"
            else:
                end_date = f"{year:04d}-{month + 1:02d}-01"
            query += " AND published_at < ?"
            params.append(end_date)

        query += """
            GROUP BY target_url
            ORDER BY link_count DESC
            LIMIT ?
        """
        params.append(limit)

        cursor.execute(query, params)

        target_urls = []
        homepage_links = 0
        deep_links = 0

        for row in cursor.fetchall():
            target_url, link_count = row

            # Determine if homepage or deep link
            # Simple heuristic: URLs ending with / or domain only are homepage
            is_homepage = target_url.rstrip("/").count("/") <= 2

            if is_homepage:
                homepage_links += link_count
            else:
                deep_links += link_count

            target_urls.append(
                {
                    "target_url": target_url,
                    "link_count": link_count,
                    "is_homepage": is_homepage,
                }
            )

        total_links = homepage_links + deep_links

        conn.close()

        return {
            "success": True,
            "data": {
                "target_urls": target_urls,
                "statistics": {
                    "total_links": total_links,
                    "unique_urls": len(target_urls),
                    "homepage_links": homepage_links,
                    "deep_links": deep_links,
                    "deep_linking_ratio": (
                        round((deep_links / total_links * 100), 2)
                        if total_links > 0
                        else 0
                    ),
                    "date_range": {"from": from_date, "to": to_date},
                },
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error analyzing target URLs: {str(e)}"
        )


@router.get("/customers/{customer_id}/link-velocity")
def get_link_velocity(
    customer_id: int,
    from_date: Optional[str] = Query(None, description="Start date (YYYY-MM)"),
    to_date: Optional[str] = Query(None, description="End date (YYYY-MM)"),
):
    """
    Analyze link acquisition velocity over time.

    Shows monthly link counts, trends, acceleration/deceleration.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Build query
        query = """
            SELECT
                strftime('%Y-%m', published_at) as month,
                COUNT(*) as link_count
            FROM customer_history
            WHERE customer_id = ?
        """
        params = [customer_id]

        # Add date filters
        from_date_parsed = parse_date(from_date)
        to_date_parsed = parse_date(to_date)

        if from_date_parsed:
            query += " AND published_at >= ?"
            params.append(from_date_parsed)

        if to_date_parsed:
            year, month = map(int, to_date_parsed.split("-")[:2])
            if month == 12:
                end_date = f"{year + 1:04d}-01-01"
            else:
                end_date = f"{year:04d}-{month + 1:02d}-01"
            query += " AND published_at < ?"
            params.append(end_date)

        query += """
            GROUP BY month
            ORDER BY month ASC
        """

        cursor.execute(query, params)

        monthly_data = []
        for row in cursor.fetchall():
            month, link_count = row
            monthly_data.append({"month": month, "link_count": link_count})

        # Calculate velocity metrics
        if len(monthly_data) >= 2:
            # Calculate trend (simple linear regression)
            total_change = (
                monthly_data[-1]["link_count"] - monthly_data[0]["link_count"]
            )
            months_span = len(monthly_data)
            avg_change_per_month = total_change / months_span if months_span > 0 else 0

            # Determine trend
            if avg_change_per_month > 2:
                trend = "accelerating"
            elif avg_change_per_month < -2:
                trend = "decelerating"
            else:
                trend = "stable"

            # Calculate average
            avg_links_per_month = sum(m["link_count"] for m in monthly_data) / len(
                monthly_data
            )
        else:
            trend = "insufficient_data"
            avg_change_per_month = 0
            avg_links_per_month = monthly_data[0]["link_count"] if monthly_data else 0

        conn.close()

        return {
            "success": True,
            "data": {
                "monthly_data": monthly_data,
                "statistics": {
                    "total_months": len(monthly_data),
                    "avg_links_per_month": round(avg_links_per_month, 2),
                    "avg_change_per_month": round(avg_change_per_month, 2),
                    "trend": trend,
                    "date_range": {"from": from_date, "to": to_date},
                },
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error analyzing link velocity: {str(e)}"
        )


@router.get("/customers/{customer_id}/domain-sources")
def get_domain_sources(
    customer_id: int,
    from_date: Optional[str] = Query(None, description="Start date (YYYY-MM)"),
    to_date: Optional[str] = Query(None, description="End date (YYYY-MM)"),
    limit: int = Query(50, ge=1, le=200),
):
    """
    Analyze which domains are providing links.

    Shows new vs returning domains, domain frequency.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Build query
        query = """
            SELECT
                pub_domain,
                COUNT(*) as link_count,
                MIN(published_at) as first_link,
                MAX(published_at) as latest_link
            FROM customer_history
            WHERE customer_id = ?
        """
        params = [customer_id]

        # Add date filters
        from_date_parsed = parse_date(from_date)
        to_date_parsed = parse_date(to_date)

        if from_date_parsed:
            query += " AND published_at >= ?"
            params.append(from_date_parsed)

        if to_date_parsed:
            year, month = map(int, to_date_parsed.split("-")[:2])
            if month == 12:
                end_date = f"{year + 1:04d}-01-01"
            else:
                end_date = f"{year:04d}-{month + 1:02d}-01"
            query += " AND published_at < ?"
            params.append(end_date)

        query += """
            GROUP BY pub_domain
            ORDER BY link_count DESC
            LIMIT ?
        """
        params.append(limit)

        cursor.execute(query, params)

        domains = []
        new_domains = 0
        returning_domains = 0

        for row in cursor.fetchall():
            pub_domain, link_count, first_link, latest_link = row

            is_new = link_count == 1
            if is_new:
                new_domains += 1
            else:
                returning_domains += 1

            domains.append(
                {
                    "pub_domain": pub_domain,
                    "link_count": link_count,
                    "first_link": first_link,
                    "latest_link": latest_link,
                    "is_new_domain": is_new,
                }
            )

        conn.close()

        return {
            "success": True,
            "data": {
                "domains": domains,
                "statistics": {
                    "total_domains": len(domains),
                    "new_domains": new_domains,
                    "returning_domains": returning_domains,
                    "new_domain_ratio": (
                        round((new_domains / len(domains) * 100), 2)
                        if len(domains) > 0
                        else 0
                    ),
                    "date_range": {"from": from_date, "to": to_date},
                },
            },
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error analyzing domain sources: {str(e)}"
        )


@router.get("/customers/{customer_id}/comparison")
def get_period_comparison(
    customer_id: int,
    period1_from: str = Query(..., description="Period 1 start date (YYYY-MM)"),
    period1_to: str = Query(..., description="Period 1 end date (YYYY-MM)"),
    period2_from: str = Query(..., description="Period 2 start date (YYYY-MM)"),
    period2_to: str = Query(..., description="Period 2 end date (YYYY-MM)"),
):
    """
    Compare link metrics between two time periods.

    Useful for before/after campaign analysis.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        def get_period_stats(from_date_str, to_date_str):
            from_date_parsed = parse_date(from_date_str)
            to_date_parsed = parse_date(to_date_str)

            if not from_date_parsed or not to_date_parsed:
                raise HTTPException(
                    status_code=400, detail="Invalid date format. Use YYYY-MM"
                )

            # Calculate end date
            year, month = map(int, to_date_parsed.split("-")[:2])
            if month == 12:
                end_date = f"{year + 1:04d}-01-01"
            else:
                end_date = f"{year:04d}-{month + 1:02d}-01"

            # Get total links
            cursor.execute(
                """
                SELECT COUNT(*) FROM customer_history
                WHERE customer_id = ?
                AND published_at >= ?
                AND published_at < ?
            """,
                (customer_id, from_date_parsed, end_date),
            )
            total_links = cursor.fetchone()[0]

            # Get unique domains
            cursor.execute(
                """
                SELECT COUNT(DISTINCT pub_domain) FROM customer_history
                WHERE customer_id = ?
                AND published_at >= ?
                AND published_at < ?
            """,
                (customer_id, from_date_parsed, end_date),
            )
            unique_domains = cursor.fetchone()[0]

            # Get unique target URLs
            cursor.execute(
                """
                SELECT COUNT(DISTINCT target_url) FROM customer_history
                WHERE customer_id = ?
                AND published_at >= ?
                AND published_at < ?
            """,
                (customer_id, from_date_parsed, end_date),
            )
            unique_urls = cursor.fetchone()[0]

            return {
                "total_links": total_links,
                "unique_domains": unique_domains,
                "unique_target_urls": unique_urls,
                "date_range": {"from": from_date_str, "to": to_date_str},
            }

        period1 = get_period_stats(period1_from, period1_to)
        period2 = get_period_stats(period2_from, period2_to)

        # Calculate changes
        changes = {
            "total_links_change": period2["total_links"] - period1["total_links"],
            "total_links_change_percent": round(
                (
                    (
                        (period2["total_links"] - period1["total_links"])
                        / period1["total_links"]
                        * 100
                    )
                    if period1["total_links"] > 0
                    else 0
                ),
                2,
            ),
            "unique_domains_change": period2["unique_domains"]
            - period1["unique_domains"],
            "unique_domains_change_percent": round(
                (
                    (
                        (period2["unique_domains"] - period1["unique_domains"])
                        / period1["unique_domains"]
                        * 100
                    )
                    if period1["unique_domains"] > 0
                    else 0
                ),
                2,
            ),
            "unique_urls_change": period2["unique_target_urls"]
            - period1["unique_target_urls"],
            "unique_urls_change_percent": round(
                (
                    (
                        (period2["unique_target_urls"] - period1["unique_target_urls"])
                        / period1["unique_target_urls"]
                        * 100
                    )
                    if period1["unique_target_urls"] > 0
                    else 0
                ),
                2,
            ),
        }

        conn.close()

        return {
            "success": True,
            "data": {"period1": period1, "period2": period2, "changes": changes},
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error comparing periods: {str(e)}"
        )
