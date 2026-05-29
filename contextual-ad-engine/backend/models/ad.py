from typing import Dict, List, Optional
from pydantic import BaseModel


class CreativeData(BaseModel):
    headline: Optional[str] = None
    body_copy: Optional[str] = None
    cta: Optional[str] = None


class AssetsData(BaseModel):
    image_url: Optional[str] = None
    gif_url: Optional[str] = None
    video_url: Optional[str] = None
    voice_url: Optional[str] = None


class AdTags(BaseModel):
    visual: Optional[str] = None
    copy_styles: List[str] = []
    tone: Optional[str] = None


class OptimizationMetadata(BaseModel):
    mode: Optional[str] = None
    directive: Optional[str] = None
    user_profile_source: Optional[str] = None
    user_profile_confidence: Optional[float] = None
    sample_size: Optional[int] = None
    rationale: Optional[str] = None


class AdCreate(BaseModel):
    ad_id: str
    brand_id: str
    product_id: Optional[str] = None
    persona_id: Optional[str] = None
    creative_data: CreativeData = CreativeData()
    assets_data: AssetsData = AssetsData()
    ad_tags: AdTags = AdTags()
    context_snapshot: Dict = {}
    optimization_metadata: OptimizationMetadata = OptimizationMetadata()
    stage: str = "pre_generated"


class AdResponse(AdCreate):
    created_at: str
