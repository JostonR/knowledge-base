from fastapi import FastAPI
from db import get_conn

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Knowledge Base API is running!"}

@app.get("/sources")
def get_sources():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sources;")
    sources = cur.fetchall()
    conn.close()
    return sources

@app.get("/source_types")
def get_sources():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM source_types;")
    sources = cur.fetchall()
    conn.close()
    return sources