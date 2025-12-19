from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CreatorCreate(BaseModel):
    full_name: str
    title: Optional[str] = None
    notes: Optional[str] = None

class CreatorRead(BaseModel):
    id: int
    full_name: str
    title: Optional[str] = None
    notes: Optional[str] = None
