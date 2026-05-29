from typing import Dict, List, Optional
from pydantic import BaseModel


class FormatPreferences(BaseModel):
    static_image: float = 0.5
    gif_template: float = 0.5
    gif_ai_multiframe: float = 0.5
    animated_banner: float = 0.5
    video_mp4: float = 0.5
    voice_audio: float = 0.5


class CopyPreferences(BaseModel):
    joke_pun: float = 0.5
    cultural_reference: float = 0.5
    question_hook: float = 0.5
    stat_hook: float = 0.5
    inspirational_quote: float = 0.5
    urgency_driven: float = 0.5
    direct_offer: float = 0.5
    story_narrative: float = 0.5
    relatable_observation: float = 0.5


class TonePreferences(BaseModel):
    warm_casual: float = 0.5
    playful_energetic: float = 0.5
    serious_premium: float = 0.5
    urgent_action: float = 0.5
    nostalgic_emotional: float = 0.5
    informative_helpful: float = 0.5


class PurchaseHistoryItem(BaseModel):
    category: str
    item: str
    count: int


class PersonaCreate(BaseModel):
    persona_id: str
    display_name: str
    age: int
    gender: str = "unspecified"
    city: str
    occupation_mode: str
    language_preference: str
    dietary: Optional[str] = None
    spending_tier: str
    persona_data: Dict = {}


class PersonaResponse(PersonaCreate):
    pass
