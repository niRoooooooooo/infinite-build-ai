import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from database import get_db

router = APIRouter(prefix="/api/ads", tags=["ads"])


class GenerateAdRequest(BaseModel):
    brand_id:   str
    product_id: str
    persona_id: str
    context:    Optional[dict] = None


@router.post("/generate")
def generate_ad(req: GenerateAdRequest, db=Depends(get_db)):
    """Placeholder — real LLM generation in Phase 4."""
    brand   = db.execute("SELECT display_name, logo_url FROM brands WHERE brand_id=?",
                         (req.brand_id,)).fetchone()
    product = db.execute("SELECT name, description, image_url FROM products WHERE product_id=?",
                         (req.product_id,)).fetchone()

    brand_name   = brand["display_name"]   if brand   else req.brand_id
    product_name = product["name"]         if product else req.product_id
    product_desc = product["description"]  if product else ""
    image_url    = product["image_url"]    if product else None

    return {
        "ad_id":      f"ad_{uuid.uuid4().hex[:12]}",
        "brand_id":   req.brand_id,
        "product_id": req.product_id,
        "persona_id": req.persona_id,
        "creative_data": {
            "headline":  f"Discover {product_name} from {brand_name}",
            "body_copy": (product_desc or "")[:100],
            "cta":       "Take the offer",
        },
        "assets_data": {
            "image_url": image_url,
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
            "directive":              "Placeholder — LLM generation in Phase 4",
            "user_profile_source":    "none",
            "user_profile_confidence": None,
            "sample_size":            0,
            "rationale":              "Phase 3 placeholder",
        },
        "stage":      "placeholder",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "_note":      "Real generation with LLM + image model implemented in Phase 4",
    }
