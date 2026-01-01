from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# -------- Inputs --------

class InsightQuoteCreate(BaseModel):
    insight_id: int = Field(..., ge=1)
    quote_id: int = Field(..., ge=1)
    note: Optional[str] = None


# -------- Core outputs (from insight_quote table) --------

class InsightQuoteOut(BaseModel):
    id: int
    insight_id: int
    quote_id: int
    note: Optional[str] = None


# -------- “View” outputs for UI helpers --------
# Matches the SELECT in list_quotes_for_insight (join into quote/source/book_reference)

class QuoteForInsightOut(BaseModel):
    insight_quote_id: int
    note: Optional[str] = None

    quote_id: int
    quote_text: str
    quote_created_at: datetime

    source_id: int
    source_name: str

    book_ref_id: Optional[int] = None
    page_start: Optional[int] = None
    page_end: Optional[int] = None
    chapter_start: Optional[int] = None
    chapter_end: Optional[int] = None


# Matches the SELECT in list_insights_for_quote (basic insight info)
# If you later want your “rich insight” shape here, we can swap this model + query.

class InsightForQuoteOut(BaseModel):
    insight_quote_id: int
    note: Optional[str] = None

    insight_id: int
    insight_content: Optional[str] = None
    insight_created_at: datetime

class InsightForQuoteRichOut(BaseModel):
    insight_quote_id: int
    insight_quote_note: Optional[str] = None

    id: int
    insight_content: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    insight_creator_id: Optional[int] = None
    insight_creator_name: Optional[str] = None

    source_id: Optional[int] = None
    source_name: Optional[str] = None

    source_creator_id: Optional[int] = None
    source_creator_name: Optional[str] = None

    source_type_id: Optional[int] = None
    source_type_name: Optional[str] = None