from fastapi import APIRouter, HTTPException
from typing import List
from db import get_conn
from schemas.insight import InsightCreate, InsightOutRead
import psycopg2.extras
from repositories.insight_repo import get_all_insights, \
    get_insight_by_id, get_series_insights, get_source_insights, create_insight

router = APIRouter(
    prefix="/insight",
    tags=["insight"]
)

@router.get("", response_model=List[InsightOutRead])
def get_insights():
    return get_all_insights()

@router.get("/source/{source_id}", response_model=List[InsightOutRead])
def source_insight(source_id: int):
    return (get_source_insights(source_id))

@router.get("/series/{series_id}", response_model=List[InsightOutRead])
def series_insight(series_id: int):
    return (get_series_insights(series_id))

@router.get("/{insight_id}", response_model=InsightOutRead)
def get_insight(insight_id: int):
    return (get_insight_by_id(insight_id))

@router.post("", response_model=InsightOutRead)
def create_single_insight(payload: InsightCreate):
    return (create_insight(payload))
