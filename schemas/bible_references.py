from pydantic import BaseModel
from typing import Optional

class BibleReferenceBase(BaseModel):
    insight_id: int
    chapter_start: Optional[int] = None
    verse_start: Optional[int] = None
    verse_end: Optional[int] = None
    chapter_end: Optional[int] = None
    bible_book_id: Optional[int] = None
    note: Optional[str] = None
    

class BibleReferenceCreate(BibleReferenceBase):
    pass

class BibleReferenceRead(BibleReferenceBase):
    id: int
    insight_content: Optional[str] = None
    insight_creator_id: Optional[int] = None
    full_name: Optional[str] = None

    source_id: Optional[int] = None
    source_name: Optional[str] = None
    series_id: Optional[int] = None
    series_name: Optional[str] = None

    bible_book_name: Optional[str] = None
    canonical_order: Optional[int] = None


