from typing import Dict
from pydantic import BaseModel


class UserPatternCreate(BaseModel):
    brand_id: str
    persona_id: str
    pattern_data: Dict = {}
    confidence: float = 0.3
    sample_size: int = 0
    updated_at: str


class UserPatternResponse(UserPatternCreate):
    pass


class OptimizationCycleCreate(BaseModel):
    cycle_id: str
    brand_id: str
    week_number: int
    events_processed: int = 0
    users_updated: int = 0
    results_summary: Dict = {}
    completed_at: str


class OptimizationCycleResponse(OptimizationCycleCreate):
    pass
