import json
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from database import get_db
from services import context_engine, generation_engine

router = APIRouter(prefix="/api/ads", tags=["ads"])


class GenerateAdRequest(BaseModel):
    brand_id:   str
    product_id: str
    persona_id: str
    context:    Optional[dict] = None


def _find_cached_ad(brand_id, product_id, persona_id, db):
    """Return a recent real_time ad from DB if it exists (< 24h old)."""
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=24)).isoformat()
    row = db.execute(
        """SELECT * FROM ads
           WHERE brand_id=? AND product_id=? AND persona_id=? AND stage='real_time'
             AND created_at > ?
           ORDER BY created_at DESC LIMIT 1""",
        (brand_id, product_id, persona_id, cutoff),
    ).fetchone()
    if not row:
        return None
    ad = dict(row)
    for f in ("creative_data", "assets_data", "ad_tags",
              "context_snapshot", "optimization_metadata"):
        ad[f] = json.loads(ad.get(f) or "{}")
    return ad


def _save_ad(ad: dict, db):
    db.execute(
        """INSERT OR REPLACE INTO ads
           (ad_id, brand_id, product_id, persona_id,
            creative_data, assets_data, ad_tags,
            context_snapshot, optimization_metadata,
            stage, created_at)
           VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
        (
            ad["ad_id"], ad["brand_id"], ad["product_id"], ad["persona_id"],
            json.dumps(ad["creative_data"]),
            json.dumps(ad["assets_data"]),
            json.dumps(ad["ad_tags"]),
            json.dumps(ad.get("context_snapshot", {})),
            json.dumps(ad.get("optimization_metadata", {})),
            ad["stage"],
            ad["created_at"],
        ),
    )
    db.commit()


@router.post("/generate")
def generate_ad(req: GenerateAdRequest, request: Request, db=Depends(get_db)):
    # Check cache first
    cached = _find_cached_ad(req.brand_id, req.product_id, req.persona_id, db)
    if cached:
        cached["_cached"] = True
        return cached

    # Build context
    client_ip = request.client.host if request.client else None
    request_info = {
        "ip":      client_ip,
        "headers": dict(request.headers),
    }
    context_obj = context_engine.get_full_context(req.persona_id, request_info, db)

    # Generate
    try:
        ad = generation_engine.compose_ad(
            req.brand_id, req.product_id, req.persona_id, context_obj, db
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    # Persist
    _save_ad(ad, db)
    return ad
