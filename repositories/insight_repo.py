from db_conn.pool import fetch_all, fetch_one

INSIGHT_SELECT_BASE = """
SELECT i.id, i.insight_content, i.created_at, i.updated_at,

ic.id AS insight_creator_id,
ic.full_name AS insight_creator_name,

s.id AS source_id,
s.source_name,

sc.id AS source_creator_id,
sc.full_name AS source_creator_name,

st.id AS source_type_id,
st.source_type_name

FROM insight i
LEFT JOIN creator ic
    ON ic.id = i.insight_creator_id

LEFT JOIN source s
    ON s.id = i.source_id

LEFT JOIN creator sc
    ON sc.id = s.creator_id

LEFT JOIN source_type st
    ON st.id = s.source_type_id
"""
Insight_FULL_LIST = (
    INSIGHT_SELECT_BASE +
    "\nORDER BY i.created_at DESC;"
)

INSIGHT_LIST_BY_SOURCE = (
    INSIGHT_SELECT_BASE +
    "\nWHERE i.source_id = %s\nORDER BY i.created_at DESC;"
)

INSIGHT_LIST_BY_SERIES = (
    INSIGHT_SELECT_BASE + 
    "\nWHERE s.series_id = %s\nORDER BY s.series_id ASC;"
)

INSIGHT_GET_BY_ID = (
    INSIGHT_SELECT_BASE +
    "\nWHERE i.id = %s;"
)

INSIGHT_CREATE = """
INSERT INTO source(
    source_id,
    insight_creator_id,
    insight_content
)
VALUES (%s, %s, %s)
RETURNING
    id,
    insight_creator_id,
    insight_content,
    created_at,
    updated_at;
"""

def get_all_insights():
    return fetch_all(Insight_FULL_LIST)

def get_series_insights(series_id: int):
    return fetch_all(INSIGHT_LIST_BY_SERIES, (series_id, ))

def get_source_insights(source_id: int):
    return fetch_all(INSIGHT_LIST_BY_SOURCE, (source_id, ))

def get_insight_by_id(insight_id: int):
    return fetch_one(INSIGHT_GET_BY_ID, (insight_id, ))

def create_insight(payload):
    params = (
        payload.source_id,
        payload.insight_creator_id,
        payload.insight_content,
    )
    return fetch_one(create_insight, params)
    