from db_conn.pool import fetch_all, fetch_one

INSIGHT_QUOTE_SELECT_BASE = """
SELECT
    iq.id,
    iq.insight_id,
    iq.quote_id,
    iq.note
FROM insight_quote iq
"""

# For UI: show quotes attached to an insight (adds quote fields + source name)
INSIGHT_QUOTES_SELECT_BASE = """
SELECT
    iq.id AS insight_quote_id,
    iq.note,

    q.id AS quote_id,
    q.quote_text,
    q.created_at AS quote_created_at,

    s.id AS source_id,
    s.source_name,

    q.book_ref_id,
    br.page_start,
    br.page_end,
    br.chapter_start,
    br.chapter_end

FROM insight_quote iq
JOIN quote q
    ON q.id = iq.quote_id
JOIN source s
    ON s.id = q.source_id
LEFT JOIN book_reference br
    ON br.id = q.book_ref_id
   AND br.source_id = q.source_id
"""

# For UI: show insights attached to a quote.
# note: replace i.<fields> with your actual insight columns / joined fields if you want “full insight detail”.
QUOTE_INSIGHTS_SELECT_BASE = """
SELECT
    iq.id AS insight_quote_id,
    iq.note,

    i.id AS insight_id,
    i.insight_content,
    i.created_at AS insight_created_at

FROM insight_quote iq
JOIN insight i
    ON i.id = iq.insight_id
"""

INSIGHT_QUOTE_CREATE = """
INSERT INTO insight_quote (insight_id, quote_id, note)
VALUES (%s, %s, %s)
RETURNING id, insight_id, quote_id, note;
"""

INSIGHT_QUOTE_GET = (
    INSIGHT_QUOTE_SELECT_BASE +
    "\nWHERE iq.id = %s;"
)

INSIGHT_QUOTE_GET_BY_PAIR = (
    INSIGHT_QUOTE_SELECT_BASE +
    "\nWHERE iq.insight_id = %s AND iq.quote_id = %s;"
)

INSIGHT_QUOTE_LIST_BY_INSIGHT = (
    INSIGHT_QUOTE_SELECT_BASE +
    "\nWHERE iq.insight_id = %s\nORDER BY iq.id DESC;"
)

INSIGHT_QUOTE_LIST_BY_QUOTE = (
    INSIGHT_QUOTE_SELECT_BASE +
    "\nWHERE iq.quote_id = %s\nORDER BY iq.id DESC;"
)

INSIGHT_QUOTE_DELETE = """
DELETE FROM insight_quote
WHERE insight_id = %s AND quote_id = %s
RETURNING id;
"""

# “View” queries (UI helpers)
INSIGHT_QUOTES_LIST = (
    INSIGHT_QUOTES_SELECT_BASE +
    "\nWHERE iq.insight_id = %s\nORDER BY iq.id DESC;"
)

QUOTE_INSIGHTS_LIST = (
    QUOTE_INSIGHTS_SELECT_BASE +
    "\nWHERE iq.quote_id = %s\nORDER BY iq.id DESC;"
)

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

# Rich “insights for quote” view:
# - join insight_quote so you can filter by quote_id
# - also return the join-table note and id (useful for UI)
QUOTE_INSIGHTS_RICH = """
SELECT
    iq.id AS insight_quote_id,
    iq.note AS insight_quote_note,

    x.*
FROM insight_quote iq
JOIN (
""" + INSIGHT_SELECT_BASE + """
) x
    ON x.id = iq.insight_id
WHERE iq.quote_id = %s
ORDER BY x.created_at DESC, x.id DESC;
"""

# -------- Functions --------

def create_insight_quote(payload):
    params = (payload.insight_id, payload.quote_id, payload.note)
    return fetch_one(INSIGHT_QUOTE_CREATE, params)


def get_insight_quote_by_id(iq_id: int):
    return fetch_one(INSIGHT_QUOTE_GET, (iq_id,))


def get_insight_quote_by_pair(insight_id: int, quote_id: int):
    return fetch_one(INSIGHT_QUOTE_GET_BY_PAIR, (insight_id, quote_id))


def list_insight_quotes_by_insight(insight_id: int):
    return fetch_all(INSIGHT_QUOTE_LIST_BY_INSIGHT, (insight_id,))


def list_insight_quotes_by_quote(quote_id: int):
    return fetch_all(INSIGHT_QUOTE_LIST_BY_QUOTE, (quote_id,))


def delete_insight_quote(insight_id: int, quote_id: int) -> bool:
    row = fetch_one(INSIGHT_QUOTE_DELETE, (insight_id, quote_id))
    return row is not None


# --- UI helpers ---
def list_quotes_for_insight(insight_id: int):
    """Return quote details (text + source + book_reference fields) for a given insight."""
    return fetch_all(INSIGHT_QUOTES_LIST, (insight_id,))


def list_insights_for_quote(quote_id: int):
    """Return insight basics for a given quote (expand to full insight detail if you want)."""
    return fetch_all(QUOTE_INSIGHTS_LIST, (quote_id,))

def list_insights_for_quote_rich(quote_id: int):
    return fetch_all(QUOTE_INSIGHTS_RICH, (quote_id,))