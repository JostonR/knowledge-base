from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from db import get_conn
from schemas.bible_references import BibleReferenceCreate, BibleReferenceRead
import psycopg2.extras
from repositories.bible_references_repo import get_bibleref, list_bibleref, list_bibleref_by_book, post_bibleref, search_bibleref_overlaps

router = APIRouter(
    prefix="/bibleref",
    tags=["bibleref"]
)

@router.get("", response_model=List[BibleReferenceRead])
def list_bible_ref():
    return list_bibleref()


# Search for insights over a bible range
@router.get("/search", response_model=List[BibleReferenceRead])
def search_bible_ref_overlap(
    book_id: int = Query(..., description="Bible book ID"),
    chapter: Optional[int] = Query(None, ge=1, description="Chapter number"),
    verse_start: Optional[int] = Query(None, ge=1),
    verse_end: Optional[int] = Query(None, ge=1)
):
    if chapter is None:
        if verse_start is not None or verse_end is not None:
            raise HTTPException(
                status_code=400,
                detail="If chapter is omitted, verse start/end must also be omitted."
            )
        return list_bibleref_by_book(book_id)
    # CASE 1: neither provided → whole chapter
    if verse_start is None and verse_end is None:
        verse_start = 1
        verse_end = 999
    # CASE 2: only verse_start is provided
    elif verse_end is None:
        verse_end = verse_start
    # CASE 3: only verse_end is provided
    elif verse_start is None:
        verse_start = 1
    if verse_end < verse_start:
        raise HTTPException(
            status_code=400,
            detail="verse_end must be greater than or equal to verse_start"
        )
    return search_bibleref_overlaps(
        book_id=book_id,
        chapter=chapter,
        verse_start=verse_start,
        verse_end=verse_end
    )

@router.get("/{bibleref_id}", response_model=BibleReferenceRead)
def get_creator(bibleref_id: int):
    return (get_bibleref(bibleref_id))

@router.post("", response_model=BibleReferenceCreate)
def create_single_source(payload: BibleReferenceCreate):
    return (post_bibleref(payload))
