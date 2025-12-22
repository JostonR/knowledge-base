from db_conn.pool import fetch_all, fetch_one

BIBLE_REF_BASE = """
SELECT br.id, br.chapter_start, br.verse_start, 
br.chapter_end, br.verse_end,

br.insight_id, i1.insight_content,
i1.insight_creator_id, c.full_name,

s.id as source_id,
s.source_name, 

s.series_id,
ser.series_name,

br.bible_book_id, b.bible_book_name, b.canonical_order

FROM bible_reference br
LEFT JOIN insight i1
    ON i1.id = br.insight_id

LEFT JOIN creator c
    ON c.id = i1.insight_creator_id

LEFT JOIN source s
    ON s.id = i1.source_id

LEFT JOIN bible_book b
    ON b.id = br.bible_book_id

LEFT JOIN series ser
    ON ser.id = s.series_id
"""
BIBLE_ORDER_BY = """ORDER BY b.canonical_order, br.chapter_start, br.verse_start ASC"""

BIBLE_REF_LIST = (BIBLE_REF_BASE + 
    "\n" + BIBLE_ORDER_BY + ";")

BIBLE_REF_LIST_BY_BOOK = (BIBLE_REF_BASE + "\nWHERE br.bible_book_id = %s\n" + BIBLE_ORDER_BY + ";")

BIBLE_REF_GET = (BIBLE_REF_BASE + 
    "\nWHERE br.id = %s" + "\n" + BIBLE_ORDER_BY + ";")

# Search: refs that overlap a query range within a single chapter
BIBLE_REF_SEARCH_OVERLAPS = (
    BIBLE_REF_BASE + 
"""
WHERE br.bible_book_id = %s
AND (
    br.chapter_start = %s
    OR br.chapter_start = %s AND br.verse_start <= %s)

AND (
    COALESCE(br.chapter_end, br.chapter_start) > %s
    OR(
        COALESCE(br.chapter_end, br.chapter_start) = %s
        AND COALESCE(br.verse_end, br.verse_start) >= %s
    )
)
"""
    + "\n" + BIBLE_ORDER_BY
    + ";"
)


BIBLE_REF_CREATE = """
INSERT INTO bible_reference (
    insight_id, 
    bible_book_id,
    chapter_start,
    verse_start,
    chapter_end,
    verse_end,
    note
)
VALUES (%s, %s, %s, %s, %s, %s, %s)
RETURNING
    id,
    insight_id,
    bible_book_id,
    chapter_start,
    verse_start,
    chapter_end,
    verse_end,
    note;
"""

def list_bibleref():
    return fetch_all(BIBLE_REF_LIST)

def list_bibleref_by_book(book_id: int):
    return fetch_all(BIBLE_REF_LIST_BY_BOOK, (book_id, ))

def get_bibleref(bibleref_int: int):
    return fetch_one(BIBLE_REF_GET, (bibleref_int, ))

def post_bibleref(payload):
    params = (
        payload.insight_id,
        payload.bible_book_id,
        payload.chapter_start,
        payload.verse_start,
        payload.chapter_end,
        payload.verse_end,
        payload.note,
    )
    return fetch_one(BIBLE_REF_CREATE, params)

def search_bibleref_overlaps(book_id: int, chapter: int, verse_start: int, verse_end: int):
    # overlaps: ref_start <= query_end AND query_start <= ref_end
    params = (
        book_id,
        chapter, chapter, verse_end,   # ref_start <= (chapter, verse_end)
        chapter, chapter, verse_start  # (chapter, verse_start) <= ref_end
    )
    return fetch_all(BIBLE_REF_SEARCH_OVERLAPS, params)
