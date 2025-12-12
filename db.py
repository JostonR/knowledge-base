import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="knowledge_base",
    user="jrod",
    password="psqlpassword"
)

print("Connected!")
conn.close()