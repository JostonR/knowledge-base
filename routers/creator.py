from fastapi import APIRouter, HTTPException
from typing import List
from db import get_conn
from schemas.creator import CreatorCreate, CreatorRead
import psycopg2.extras
from repositories.creator_repo import list_creators_get, creator_get, creator_post_creator

router = APIRouter(
    prefix="/creator",
    tags=["creator"]
)

@router.get("", response_model=List[CreatorRead])
def list_creators():
    return list_creators_get()

@router.get("/{creator_id}", response_model=CreatorRead)
def get_creator(creator_id: int):
    return (creator_get(creator_id))

@router.post("", response_model=CreatorCreate)
def create_single_source(payload: CreatorCreate):
    return (creator_post_creator(payload))
