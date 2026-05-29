from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from database import get_db
from services.event_logger import log_conversion_event

router = APIRouter(prefix="/api/events", tags=["events"])


class ConversionEventRequest(BaseModel):
    ad_id:             str
    persona_id:        str
    converted:         bool
    conversion_source: str = "live_interaction"
    brand_id:          Optional[str] = None
    context_snapshot:  Optional[dict] = None
    persona_snapshot:  Optional[dict] = None
    ad_tags:           Optional[dict] = None


@router.post("")
def log_event(req: ConversionEventRequest, db=Depends(get_db)):
    brand_id = req.brand_id
    if not brand_id:
        row = db.execute(
            "SELECT brand_id FROM ads WHERE ad_id=?", (req.ad_id,)
        ).fetchone()
        brand_id = row["brand_id"] if row else "unknown"

    # Build persona snapshot from DB if not provided
    persona_snapshot = req.persona_snapshot or {}
    if not persona_snapshot:
        row = db.execute(
            "SELECT age, city, occupation_mode, spending_tier FROM personas WHERE persona_id=?",
            (req.persona_id,),
        ).fetchone()
        if row:
            age = row["age"]
            if age < 18:
                bracket = "under_18"
            elif age <= 25:
                bracket = "18_25"
            elif age <= 40:
                bracket = "26_40"
            elif age <= 55:
                bracket = "41_55"
            else:
                bracket = "55_plus"
            persona_snapshot = {
                "age_bracket":    bracket,
                "city":           row["city"],
                "occupation_mode": row["occupation_mode"],
                "spending_tier":  row["spending_tier"],
            }

    event_id = log_conversion_event(
        ad_id=req.ad_id,
        persona_id=req.persona_id,
        brand_id=brand_id,
        context=req.context_snapshot or {},
        ad_tags=req.ad_tags or {},
        converted=req.converted,
        source=req.conversion_source,
        persona_snapshot=persona_snapshot,
        db=db,
    )

    return {"event_id": event_id, "status": "logged"}
