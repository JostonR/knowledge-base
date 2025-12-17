from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InsightCreateBase(BaseModel):
    source_id: int
    insight_content: str
    insight_creator_id: Optional[int] = None

class InsightCreate(InsightCreateBase):
    pass

class InsightOutRead(BaseModel):
    id: int
    insight_creator_name: Optional[str] = None
    source_name: Optional[str] = None
    insight_content: str
    source_type_name: Optional[str] = None
    source_creator_name: Optional[str] = None
    insight_creator_id: Optional[int] = None
    source_type_id: Optional[int] = None
    source_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None 


