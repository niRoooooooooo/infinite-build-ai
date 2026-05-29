from typing import List, Optional
from pydantic import BaseModel


class VoiceData(BaseModel):
    tone: Optional[str] = None
    personality: Optional[str] = None
    language_style: Optional[str] = None
    key_messages: Optional[List[str]] = None


class VisualData(BaseModel):
    primary_color: Optional[str] = None
    accent_color: Optional[str] = None
    secondary_color: Optional[str] = None
    style: Optional[str] = None


class ConstraintsData(BaseModel):
    avoid_topics: Optional[List[str]] = None
    avoid_tones: Optional[List[str]] = None
    max_price_mention: Optional[bool] = None


class BrandCreate(BaseModel):
    brand_id: str
    display_name: str
    tagline: Optional[str] = None
    description: Optional[str] = None
    logo_url: Optional[str] = None
    voice_data: VoiceData = VoiceData()
    visual_data: VisualData = VisualData()
    constraints_data: ConstraintsData = ConstraintsData()


class BrandResponse(BrandCreate):
    created_at: str
