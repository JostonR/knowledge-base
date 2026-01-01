from fastapi import APIRouter, HTTPException
from typing import List
from db import get_conn
from schemas.quote import QuoteCreate, QuoteDetailOut, QuoteOut
import psycopg2.extras
from repositories.quote_repo import get_all_quotes_from_source, get_quote_from_id, create_quote, delete_quote, list_quotes

router = APIRouter(
    prefix="/quote",
    tags=["quote"]
)

@router.get("", response_model=List[QuoteDetailOut])
def get_quotes():
    return list_quotes()

@router.get("/source/{source_id}", response_model=List[QuoteDetailOut])
def get_source_quote(source_id: int):
    return (get_all_quotes_from_source(source_id))

@router.get("/{quote_id}", response_model=QuoteDetailOut)
def get_quote_id(quote_id: int):
    quote = get_quote_from_id(quote_id)
    if quote is None:
        raise HTTPException(status_code=404, detail="Quote not found")
    return quote

@router.post("", response_model=QuoteOut)
def quote_create(payload: QuoteCreate):
    return (create_quote(payload))

@router.delete("/{quote_id}", status_code=204)
def quote_delete(quote_id: int):
    ok = delete_quote(quote_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Quote not found")
    return None