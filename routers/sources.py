from fastapi import APIRouter, HTTPException
from typing import List
from db import get_conn
from schemas.source import SourceCreate, SourceOut
import psycopg2.extras
from repositories.source_repo import list_sources, get_source, create_source

router = APIRouter(
    prefix="/source",
    tags=["source"]
)

@router.get("", response_model=List[SourceOut])
def get_sources():
    return list_sources()

@router.get("/{source_id}", response_model=SourceOut)
def get_single_source(source_id: int):
    return (get_source(source_id))

@router.post("", response_model=SourceOut)
def create_single_source(payload: SourceCreate):
    return (create_source(payload))
