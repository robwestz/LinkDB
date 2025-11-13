"""
CRUD Operations for LinkDB

Provides endpoints to Create, Read, Update, and Delete links in the database.
Enables live editing from the frontend.
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/links", tags=["crud"])

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


# Pydantic models for request/response
class LinkCreate(BaseModel):
    customer_id: int
    canonical_root: str
    brand: str
    pub_domain: str
    target_url: str
    anchor_text: str
    published_at: str  # Format: YYYY-MM-DD


class LinkUpdate(BaseModel):
    pub_domain: Optional[str] = None
    target_url: Optional[str] = None
    anchor_text: Optional[str] = None
    published_at: Optional[str] = None


class LinkResponse(BaseModel):
    id: int
    customer_id: int
    canonical_root: str
    brand: str
    pub_domain: str
    target_url: str
    anchor_text: str
    published_at: str


@router.post("/", response_model=dict)
def create_link(link: LinkCreate):
    """
    Create a new link entry in the database.

    This adds a new link to the customer's history.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Validate date format
        try:
            datetime.strptime(link.published_at, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(
                status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
            )

        # Insert new link
        cursor.execute(
            """
            INSERT INTO customer_history
            (customer_id, canonical_root, brand, pub_domain, target_url, anchor_text, published_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
            (
                link.customer_id,
                link.canonical_root,
                link.brand,
                link.pub_domain,
                link.target_url,
                link.anchor_text,
                link.published_at,
            ),
        )

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return {
            "success": True,
            "message": "Link created successfully",
            "data": {"id": new_id, **link.dict()},
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating link: {str(e)}")


@router.get("/{link_id}", response_model=dict)
def get_link(link_id: int):
    """
    Get a specific link by ID.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT rowid, customer_id, canonical_root, brand, pub_domain, target_url, anchor_text, published_at
            FROM customer_history
            WHERE rowid = ?
        """,
            (link_id,),
        )

        row = cursor.fetchone()
        conn.close()

        if not row:
            raise HTTPException(
                status_code=404, detail=f"Link with ID {link_id} not found"
            )

        return {
            "success": True,
            "data": {
                "id": row[0],
                "customer_id": row[1],
                "canonical_root": row[2],
                "brand": row[3],
                "pub_domain": row[4],
                "target_url": row[5],
                "anchor_text": row[6],
                "published_at": row[7],
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching link: {str(e)}")


@router.put("/{link_id}", response_model=dict)
def update_link(link_id: int, link_update: LinkUpdate):
    """
    Update an existing link.

    Only provided fields will be updated. Others remain unchanged.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if link exists
        cursor.execute("SELECT rowid FROM customer_history WHERE rowid = ?", (link_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404, detail=f"Link with ID {link_id} not found"
            )

        # Build update query dynamically
        update_fields = []
        params = []

        if link_update.pub_domain is not None:
            update_fields.append("pub_domain = ?")
            params.append(link_update.pub_domain)

        if link_update.target_url is not None:
            update_fields.append("target_url = ?")
            params.append(link_update.target_url)

        if link_update.anchor_text is not None:
            update_fields.append("anchor_text = ?")
            params.append(link_update.anchor_text)

        if link_update.published_at is not None:
            # Validate date format
            try:
                datetime.strptime(link_update.published_at, "%Y-%m-%d")
            except ValueError:
                raise HTTPException(
                    status_code=400, detail="Invalid date format. Use YYYY-MM-DD"
                )

            update_fields.append("published_at = ?")
            params.append(link_update.published_at)

        if not update_fields:
            raise HTTPException(status_code=400, detail="No fields to update")

        # Execute update
        params.append(link_id)
        query = (
            f"UPDATE customer_history SET {', '.join(update_fields)} WHERE rowid = ?"
        )
        cursor.execute(query, params)

        conn.commit()

        # Fetch updated link
        cursor.execute(
            """
            SELECT rowid, customer_id, canonical_root, brand, pub_domain, target_url, anchor_text, published_at
            FROM customer_history
            WHERE rowid = ?
        """,
            (link_id,),
        )

        row = cursor.fetchone()
        conn.close()

        return {
            "success": True,
            "message": "Link updated successfully",
            "data": {
                "id": row[0],
                "customer_id": row[1],
                "canonical_root": row[2],
                "brand": row[3],
                "pub_domain": row[4],
                "target_url": row[5],
                "anchor_text": row[6],
                "published_at": row[7],
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating link: {str(e)}")


@router.delete("/{link_id}", response_model=dict)
def delete_link(link_id: int):
    """
    Delete a link from the database.

    WARNING: This permanently removes the link. Cannot be undone.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if link exists
        cursor.execute("SELECT rowid FROM customer_history WHERE rowid = ?", (link_id,))
        if not cursor.fetchone():
            raise HTTPException(
                status_code=404, detail=f"Link with ID {link_id} not found"
            )

        # Delete link
        cursor.execute("DELETE FROM customer_history WHERE rowid = ?", (link_id,))
        conn.commit()
        conn.close()

        return {"success": True, "message": f"Link {link_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting link: {str(e)}")


@router.post("/bulk-delete", response_model=dict)
def bulk_delete_links(link_ids: list[int]):
    """
    Delete multiple links at once.

    Useful for cleaning up multiple entries.
    """
    try:
        if not link_ids:
            raise HTTPException(status_code=400, detail="No link IDs provided")

        conn = get_db_connection()
        cursor = conn.cursor()

        # Delete links
        placeholders = ",".join("?" * len(link_ids))
        cursor.execute(
            f"DELETE FROM customer_history WHERE rowid IN ({placeholders})", link_ids
        )

        deleted_count = cursor.rowcount
        conn.commit()
        conn.close()

        return {
            "success": True,
            "message": f"Deleted {deleted_count} link(s)",
            "data": {"deleted_count": deleted_count},
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error bulk deleting links: {str(e)}"
        )
