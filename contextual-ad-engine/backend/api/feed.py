import json
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException

from database import get_db

router = APIRouter(prefix="/api", tags=["feed"])

_ORGANIC_PATH = Path(__file__).parent.parent.parent / "data" / "organic_feed.json"
_organic_cache = None


def _load_organic() -> list:
    global _organic_cache
    if _organic_cache is None:
        with open(_ORGANIC_PATH) as f:
            _organic_cache = json.load(f)
    return _organic_cache


def _placeholder_ad(brand: dict, product: dict, persona_id: str) -> dict:
    """Minimal placeholder — real generation in Phase 4."""
    return {
        "ad_id": f"placeholder_{brand['brand_id']}_{product['product_id']}",
        "brand": {
            "brand_id":    brand["brand_id"],
            "display_name": brand["display_name"],
            "logo_url":    brand.get("logo_url"),
        },
        "creative_data": {
            "headline":  f"Try {product['name']} — from {brand['display_name']}",
            "body_copy": (product.get("description") or "")[:80],
            "cta":       "Take the offer",
        },
        "assets_data": {
            "image_url": product.get("image_url"),
            "gif_url":   None,
            "video_url": None,
            "voice_url": None,
        },
        "ad_tags": {
            "visual":      "static_image",
            "copy_styles": ["direct_offer"],
            "tone":        "warm_casual",
        },
        "optimization_metadata": {
            "mode":                   "placeholder",
            "directive":              "Phase 4 pending",
            "user_profile_source":    "none",
            "user_profile_confidence": None,
            "sample_size":            0,
            "rationale":              "Placeholder ad — LLM generation in Phase 4",
        },
        "stage":      "placeholder",
        "persona_id": persona_id,
    }


@router.get("/organic-feed")
def organic_feed():
    return _load_organic()


@router.get("/feed/{persona_id}")
def personalized_feed(persona_id: str, db=Depends(get_db)):
    if not db.execute(
        "SELECT 1 FROM personas WHERE persona_id=?", (persona_id,)
    ).fetchone():
        raise HTTPException(404, f"Persona '{persona_id}' not found")

    organic = [{"type": "organic", **card} for card in _load_organic()]

    # Build one placeholder sponsored card per brand
    brand_rows = db.execute("SELECT * FROM brands ORDER BY brand_id").fetchall()
    sponsored = []
    for br in brand_rows:
        brand = dict(br)
        for f in ("voice_data", "visual_data", "constraints_data"):
            if brand.get(f):
                brand[f] = json.loads(brand[f])

        prod_row = db.execute(
            "SELECT * FROM products WHERE brand_id=? LIMIT 1", (brand["brand_id"],)
        ).fetchone()
        if not prod_row:
            continue
        product = dict(prod_row)
        product["target_audience"] = json.loads(product.get("target_audience") or "{}")
        sponsored.append({
            "type": "sponsored",
            **_placeholder_ad(brand, product, persona_id),
        })

    # Interleave: 3 organic, 1 sponsored, 2 organic, 1 sponsored, …
    feed, oi, si, slot = [], 0, 0, 0
    while oi < len(organic) or si < len(sponsored):
        count = 3 if slot % 2 == 0 else 2
        for _ in range(count):
            if oi < len(organic):
                feed.append(organic[oi]); oi += 1
        if si < len(sponsored):
            feed.append(sponsored[si]); si += 1
        slot += 1

    return {"persona_id": persona_id, "feed": feed, "total": len(feed)}
