from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from database import get_db

router = APIRouter(prefix="/api/optimization", tags=["optimization"])


class RunCycleRequest(BaseModel):
    brand_id: Optional[str] = None


@router.post("/run-cycle")
def run_cycle(req: RunCycleRequest = RunCycleRequest(), db=Depends(get_db)):
    """Placeholder — real optimization logic in Phase 5."""
    event_count  = db.execute("SELECT COUNT(*) FROM conversion_events").fetchone()[0]
    persona_count = db.execute("SELECT COUNT(*) FROM personas").fetchone()[0]

    return {
        "status":             "cycle_complete",
        "events_processed":   event_count,
        "users_updated":      persona_count,
        "new_recommendations": 0,
        "steps_completed": [
            "Extracting user patterns...",
            "Aggregating insights...",
            "Reshaping libraries...",
            "Generating recommendations...",
            "Complete.",
        ],
        "_note": "Placeholder — real optimization logic implemented in Phase 5",
    }
