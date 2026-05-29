import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request

from database import get_db
from services import context_engine, generation_engine

router = APIRouter(prefix="/api", tags=["feed"])

_ORGANIC_PATH  = Path(__file__).parent.parent.parent / "data" / "organic_feed.json"
_organic_cache = None
_MAX_SPONSORED  = 3


def _load_organic() -> list:
    global _organic_cache
    if _organic_cache is None:
        with open(_ORGANIC_PATH) as f:
            _organic_cache = json.load(f)
    return _organic_cache


def _find_cached_ad(brand_id, product_id, persona_id, db):
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


def _get_sponsored_slot(brand, product, persona_id, context_obj, db) -> dict:
    """Return a real (or cached) ad for one sponsored slot."""
    brand_id   = brand["brand_id"]
    product_id = product["product_id"]

    cached = _find_cached_ad(brand_id, product_id, persona_id, db)
    if cached:
        cached["_cached"] = True
        return {"type": "sponsored", **cached}

    try:
        ad = generation_engine.compose_ad(
            brand_id, product_id, persona_id, context_obj, db
        )
        _save_ad(ad, db)
        return {"type": "sponsored", **ad}
    except Exception as exc:
        # Graceful degradation — skip this slot rather than crash
        import logging
        logging.getLogger(__name__).error(
            "Sponsored slot generation failed for %s: %s", brand_id, exc
        )
        return None


@router.get("/organic-feed")
def organic_feed():
    return _load_organic()


@router.get("/feed/{persona_id}")
def personalized_feed(persona_id: str, request: Request, db=Depends(get_db)):
    if not db.execute(
        "SELECT 1 FROM personas WHERE persona_id=?", (persona_id,)
    ).fetchone():
        raise HTTPException(404, f"Persona '{persona_id}' not found")

    organic = [{"type": "organic", **card} for card in _load_organic()]

    # Build context once — shared across all sponsored slots
    client_ip = request.client.host if request.client else None
    request_info = {"ip": client_ip, "headers": dict(request.headers)}
    context_obj = context_engine.get_full_context(persona_id, request_info, db)

    # Pick up to _MAX_SPONSORED brands (one product each, different brands)
    brand_rows = db.execute(
        "SELECT * FROM brands ORDER BY brand_id"
    ).fetchall()

    sponsored = []
    for br in brand_rows:
        if len(sponsored) >= _MAX_SPONSORED:
            break

        brand = dict(br)
        for f in ("voice_data", "visual_data", "constraints_data"):
            if brand.get(f):
                brand[f] = json.loads(brand[f])

        prod_row = db.execute(
            "SELECT * FROM products WHERE brand_id=? LIMIT 1",
            (brand["brand_id"],),
        ).fetchone()
        if not prod_row:
            continue

        product = dict(prod_row)

        slot = _get_sponsored_slot(brand, product, persona_id, context_obj, db)
        if slot:
            sponsored.append(slot)

    # Interleave: 3 organic, 1 sponsored, 2 organic, 1 sponsored, …
    feed, oi, si, slot_num = [], 0, 0, 0
    while oi < len(organic) or si < len(sponsored):
        count = 3 if slot_num % 2 == 0 else 2
        for _ in range(count):
            if oi < len(organic):
                feed.append(organic[oi])
                oi += 1
        if si < len(sponsored):
            feed.append(sponsored[si])
            si += 1
        slot_num += 1

    return {"persona_id": persona_id, "feed": feed, "total": len(feed)}
