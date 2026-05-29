import json

from fastapi import APIRouter, Depends, HTTPException

from database import get_db

router = APIRouter(prefix="/api/personas", tags=["personas"])


def _row(row) -> dict:
    d = dict(row)
    d["persona_data"] = json.loads(d.get("persona_data") or "{}")
    return d


@router.get("")
def list_personas(db=Depends(get_db)):
    rows = db.execute("SELECT * FROM personas ORDER BY display_name").fetchall()
    return [_row(r) for r in rows]


@router.get("/{persona_id}")
def get_persona(persona_id: str, db=Depends(get_db)):
    row = db.execute(
        "SELECT * FROM personas WHERE persona_id=?", (persona_id,)
    ).fetchone()
    if not row:
        raise HTTPException(404, f"Persona '{persona_id}' not found")
    return _row(row)
