from fastapi import APIRouter, Depends, HTTPException, Request

from database import get_db
from services.context_engine import get_full_context

router = APIRouter(prefix="/api/context", tags=["context"])


@router.get("/{persona_id}")
def get_context(persona_id: str, request: Request, db=Depends(get_db)):
    if not db.execute(
        "SELECT 1 FROM personas WHERE persona_id=?", (persona_id,)
    ).fetchone():
        raise HTTPException(404, f"Persona '{persona_id}' not found")

    request_info = {
        "ip":      request.client.host if request.client else None,
        "headers": dict(request.headers),
    }

    return get_full_context(persona_id, request_info, db)
