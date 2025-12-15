from fastapi import FastAPI
from db import get_conn
from routers import sources
from repositories.source_repo import list_sources, get_source
from routers.api import api_router

app = FastAPI()
app.include_router(api_router)

@app.get("/")
def root():
    return {"message": "Knowledge Base API is running!"}

@app.get("/source_type")
def get_sources():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM source_type;")
    sources = cur.fetchall()
    conn.close()
    return sources
