# routers/debug.py
from fastapi import APIRouter, HTTPException
from db_conn.pool import fetch_all
import os

router = APIRouter(
    prefix="/debug",
    tags=["debug"]
)

@router.get("/dump")
def dump_all_tables():
    if os.getenv("ENV", "development") != "development":
        raise HTTPException(status_code=404, detail="Not found")
    
    tables = fetch_all("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
          AND table_type = 'BASE TABLE'
        ORDER BY table_name;
    """)

    result = {}
    for t in tables:
        table_name = t["table_name"]
        result[table_name] = fetch_all(f'SELECT * FROM "{table_name}";')

    return result
