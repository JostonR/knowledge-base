from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SourceCreate(BaseModel):
    source_name: str
    source_type_id: int
    series: Optional[int] = None
    creator_id: Optional[int] = None
    secondary_creator_id: Optional[int] = None
    source_description: Optional[str] = None

class SourceOut(BaseModel):
    id: int
    source_name: str
    source_type_id: int
    series: Optional[int] = None
    creator_id: Optional[int] = None
    secondary_creator_id: Optional[int] = None
    source_description: Optional[str] = None
    created_at: Optional[datetime] = None 
    updated_at: Optional[datetime] = None 