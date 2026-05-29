from typing import List, Optional
from pydantic import BaseModel


class TargetAudience(BaseModel):
    age_range: Optional[str] = None
    occupation: Optional[List[str]] = None
    city: Optional[List[str]] = None
    dietary: Optional[List[str]] = None


class ProductCreate(BaseModel):
    product_id: str
    brand_id: str
    name: str
    category: str
    description: Optional[str] = None
    image_url: Optional[str] = None
    target_audience: TargetAudience = TargetAudience()


class ProductResponse(ProductCreate):
    created_at: str
