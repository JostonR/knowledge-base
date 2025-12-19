from fastapi import APIRouter, HTTPException
from typing import List
from db import get_conn
from schemas.bible_references import BibleReferenceCreate, BibleReferenceRead
import psycopg2.extras
from repositories.bible_references_repo import get_bibleref, list_bibleref, post_bibleref

router = APIRouter(
    prefix="/bibleref",
    tags=["bibleref"]
)

@router.get("", response_model=List[BibleReferenceRead])
def list_bible_ref():
    return list_bibleref()

@router.get("/{bibleref_id}", response_model=BibleReferenceRead)
def get_creator(bibleref_id: int):
    return (get_bibleref(bibleref_id))

@router.post("", response_model=BibleReferenceCreate)
def create_single_source(payload: BibleReferenceCreate):
    return (post_bibleref(payload))
