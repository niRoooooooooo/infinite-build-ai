from typing import Dict, Optional
from pydantic import BaseModel


class ContextSnapshot(BaseModel):
    city: Optional[str] = None
    weather: Optional[str] = None
    temp_c: Optional[float] = None
    time_bucket: Optional[str] = None
    day_of_week: Optional[str] = None
    season: Optional[str] = None
    cultural_moment: Optional[str] = None
    derived_mood: Optional[str] = None


class PersonaSnapshot(BaseModel):
    age_bracket: Optional[str] = None
    city: Optional[str] = None
    occupation_mode: Optional[str] = None
    spending_tier: Optional[str] = None


class ConversionEventCreate(BaseModel):
    event_id: str
    timestamp: str
    ad_id: str
    brand_id: str
    persona_id: str
    context_snapshot: ContextSnapshot = ContextSnapshot()
    persona_snapshot: PersonaSnapshot = PersonaSnapshot()
    ad_tags: Dict = {}
    converted: int
    conversion_source: str


class ConversionEventResponse(ConversionEventCreate):
    pass
