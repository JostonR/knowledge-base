from db_conn.pool import fetch_all, fetch_one

CREATOR_LIST = """
SELECT id, full_name, title, notes 
FROM creator
ORDER BY full_name ASC;
"""

CREATOR_GET = """
SELECT id, full_name, title, notes 
FROM creator
WHERE s.id = %s;
"""

CREATOR_CREATE = """
INSERT INTO creator (
    full_name, 
    title,
    notes
)
VALUES (%s, %s, %s)
RETURNING
    id,
    full_name,
    title,
    notes;
"""

def list_creators_get():
    return fetch_all(CREATOR_LIST)

def creator_get(creator_id: int):
    return fetch_one(CREATOR_GET, (creator_id, ))

def creator_post_creator(payload):
    params = (
        payload.full_name,
        payload.title,
        payload.notes,
    )
    return fetch_one(CREATOR_CREATE, params)
    