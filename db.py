import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="knowledge_base",
    user="jrod",
    password="psqlpassword"
)

print("Connected!")
conn.close()

import psycopg2
from psycopg2.extras import RealDictCursor

def get_conn():
    return psycopg2.connect(
        host="localhost",
        database="knowledge_base",
        user="jostonrodrigues",
       # password="psqlpassword",
        cursor_factory=RealDictCursor
    )
