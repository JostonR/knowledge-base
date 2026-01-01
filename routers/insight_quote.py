from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query

from schemas.insight_quote import (
    InsightQuoteCreate,
    InsightQuoteOut,
    QuoteForInsightOut,
    InsightForQuoteOut,
    InsightForQuoteRichOut,
)

from repositories.insight_quote_repo import (
    create_insight_quote,
    get_insight_quote_by_id,
    get_insight_quote_by_pair,
    list_insight_quotes_by_insight,
    list_insight_quotes_by_quote,
    delete_insight_quote,
    list_quotes_for_insight,
    list_insights_for_quote,
    list_insights_for_quote_rich,
)

router = APIRouter(
    prefix="/insight-quotes",
    tags=["insight_quotes"],
)


@router.post("", response_model=InsightQuoteOut, status_code=201)
def attach_quote_to_insight(payload: InsightQuoteCreate):
    """
    Creates a link between an insight and a quote.
    Enforced unique(insight_id, quote_id) at DB level.
    """
    try:
        row = create_insight_quote(payload)
        if row is None:
            # should never happen if RETURNING works
            raise HTTPException(status_code=500, detail="Failed to create insight_quote link")
        return row
    except Exception as e:
        msg = str(e).lower()

        # Unique constraint violation (duplicate link)
        if "unique" in msg and "insight_id" in msg and "quote_id" in msg:
            raise HTTPException(status_code=409, detail="This quote is already attached to this insight")

        # FK violations (bad IDs)
        if "foreign key" in msg:
            raise HTTPException(status_code=400, detail="Invalid insight_id or quote_id")

        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{insight_quote_id}", response_model=InsightQuoteOut)
def get_insight_quote_link(insight_quote_id: int):
    row = get_insight_quote_by_id(insight_quote_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Insight-Quote link not found")
    return row


@router.get("", response_model=List[InsightQuoteOut])
def list_links(
    insight_id: Optional[int] = Query(None, ge=1),
    quote_id: Optional[int] = Query(None, ge=1),
):
    """
    List raw links. Provide either insight_id or quote_id.
    """
    if insight_id is None and quote_id is None:
        raise HTTPException(status_code=400, detail="Provide insight_id or quote_id")

    if insight_id is not None and quote_id is not None:
        # If both are provided, return the single link (if it exists) as a 1-item list
        row = get_insight_quote_by_pair(insight_id, quote_id)
        return [row] if row else []

    if insight_id is not None:
        return list_insight_quotes_by_insight(insight_id)

    return list_insight_quotes_by_quote(quote_id)


@router.delete("", status_code=204)
def detach_quote_from_insight(
    insight_id: int = Query(..., ge=1),
    quote_id: int = Query(..., ge=1),
):
    """
    Detach (delete link) by composite key.
    Example: DELETE /insight-quotes?insight_id=1&quote_id=2
    """
    ok = delete_insight_quote(insight_id, quote_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Insight-Quote link not found")
    return None


# ---------- UI helper endpoints ----------

@router.get("/insight/{insight_id}/quotes", response_model=List[QuoteForInsightOut])
def get_quotes_for_insight(insight_id: int):
    """
    For an Insight detail screen: show all attached quotes with quote text + source + book_reference fields.
    """
    return list_quotes_for_insight(insight_id)


@router.get("/quote/{quote_id}/insights", response_model=List[InsightForQuoteRichOut])
def get_insights_for_quote(quote_id: int):
    """
    For a Quote detail screen: show all insights that reference this quote (basic insight fields).
    """
    return list_insights_for_quote_rich(quote_id)
