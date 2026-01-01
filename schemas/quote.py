from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class QuoteCreate(BaseModel):
    quote_text: str = Field(..., min_length=1)
    source_id: int = Field(..., ge=1)
    book_ref_id: Optional[int] = Field(None, ge=1)

class QuoteOut(BaseModel):
    id: int
    quote_text: str
    source_id: int
    book_ref_id: Optional[int] = None
    created_at: datetime

class QuoteDetailOut(BaseModel):
    id: int
    quote_text: str
    created_at: datetime

    source_id: int
    source_name: str

    book_ref_id: Optional[int] = None
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    chapter_start: Optional[int] = None
    chapter_end: Optional[int] = None
