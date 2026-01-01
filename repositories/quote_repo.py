from db_conn.pool import fetch_all, fetch_one

QUOTE_SELECT_BASE = """
SELECT
    q.id,
    q.quote_text,
    q.created_at,

    s.id AS source_id,
    s.source_name,

    q.book_ref_id,

    br.page_start,
    br.page_end,
    br.chapter_start,
    br.chapter_end

FROM quote q
JOIN source s
    ON s.id = q.source_id
LEFT JOIN book_reference br
    ON br.id = q.book_ref_id
    AND br.source_id = q.source_id
"""

QUOTE_LIST = (
    QUOTE_SELECT_BASE +
    "\nORDER BY s.source_name ASC"
)

QUOTE_ID = (
    QUOTE_SELECT_BASE + 
    "\nWHERE q.id = %s;"
)

QUOTE_SOURCE = (
    QUOTE_SELECT_BASE + 
    "\nWHERE s.id = %s" + 
    "\nORDER BY q.created_at DESC;"
)

QUOTE_CREATE = """
INSERT INTO quote (
    quote_text,
    source_id,
    book_ref_id
)
VALUES (%s, %s, %s)
Returning
    id,
    quote_text,
    source_id,
    book_ref_id,
    created_at;
"""

QUOTE_DELETE = """
DELETE FROM quote
WHERE id = %s
RETURNING id;
"""

def list_quotes():
    return fetch_all(QUOTE_LIST)

def get_all_quotes_from_source(source_id: int):
    return fetch_all(QUOTE_SOURCE, (source_id, ))

def get_quote_from_id(quote_id: int):
    return fetch_one(QUOTE_ID, (quote_id, ))

def create_quote(payload):
    params = (
       payload.quote_text,
       payload.source_id,
       payload.book_ref_id,
    )
    return fetch_one(QUOTE_CREATE, params)

def delete_quote(quote_id: int) -> bool:
    row = fetch_one(QUOTE_DELETE, (quote_id, ))
    return row is not None