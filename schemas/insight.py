from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class InsightCreate(BaseModel):
    source_id: int
    insight_content: str
    insight_creator_id: Optional[int] = None

class InsightOut(BaseModel):
    id: int
    source_id: int
    insight_content: str
    insight_creator_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None 