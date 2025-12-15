from db_conn.pool import fetch_all, fetch_one

SOURCE_LIST = """
SELECT s.id, s.source_name, s.series, s.source_description, s.created_at, s.updated_at,

s.creator_id, c1.full_name AS creator_full_name,
s.secondary_creator_id, c2.full_name AS secondary_creator_full_name,

s.source_type_id, st.source_type_name AS source_type_name

FROM source s
LEFT JOIN creator c1
    ON c1.id = s.creator_id
LEFT JOIN creator c2
    ON c2.id = s.secondary_creator_id
LEFT JOIN source_type st
    ON st.id = s.source_type_id

ORDER BY s.created_at DESC;
"""

SOURCE_GET = """
SELECT s.id, s.source_name, s.series, s.source_description, s.created_at, s.updated_at,

s.creator_id, c1.full_name AS creator_full_name,
s.secondary_creator_id, c2.full_name AS secondary_creator_full_name,

s.source_type_id, st.source_type_name AS source_type_name

FROM source s
LEFT JOIN creator c1
    ON c1.id = s.creator_id
LEFT JOIN creator c2
    ON c2.id = s.secondary_creator_id
LEFT JOIN source_type st
    ON st.id = s.source_type_id

WHERE s.id = %s;
"""

SOURCE_CREATE = """
INSERT INTO source (
    source_name,
    source_type_id,
    series,
    creator_id,
    secondary_creator_id,
    source_description
)
VALUES (%s, %s, %s, %s, %s, %s)
RETURNING
    id,
    source_name,
    source_type_id,
    series,
    creator_id,
    secondary_creator_id,
    source_description,
    created_at,
    updated_at;
"""

def list_sources():
    return fetch_all(SOURCE_LIST)

def get_source(source_id: int):
    return fetch_one(SOURCE_GET, (source_id, ))

def create_source(payload):
    params = (
        payload.source_name,
        payload.source_type_id,
        payload.series,
        payload.creator_id,
        payload.secondary_creator_id,
        payload.source_description,
    )
    return fetch_one(SOURCE_CREATE, params)
    