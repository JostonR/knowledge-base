import pytest
from fastapi.testclient import TestClient
import psycopg2.extras

# ✅ Adjust this import to wherever your FastAPI app instance lives.
# Common options:
# from app.main import app
# from main import app
from main import app

from db import get_conn

client = TestClient(app)

BASE = "/api/quote"  # if your API prefix differs, change this to "/quote" etc.


def _get_existing_source_and_bookref():
    """
    Find a usable source_id from the DB and (optionally) a book_ref_id that matches that source_id.
    This avoids hardcoding seeded IDs.
    """
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id FROM source ORDER BY id ASC LIMIT 1;")
            src = cur.fetchone()

            if not src:
                return None, None

            source_id = src["id"]

            cur.execute(
                """
                SELECT id
                FROM book_reference
                WHERE source_id = %s
                ORDER BY id ASC
                LIMIT 1;
                """,
                (source_id,),
            )
            br = cur.fetchone()
            book_ref_id = br["id"] if br else None

    return source_id, book_ref_id


@pytest.fixture()
def existing_source_and_bookref():
    source_id, book_ref_id = _get_existing_source_and_bookref()
    if source_id is None:
        pytest.skip("No source rows found in DB; seed your database before running quote tests.")
    return source_id, book_ref_id


@pytest.fixture()
def created_quote_id(existing_source_and_bookref):
    """
    Create a quote through the API and yield its ID.
    Cleanup tries to delete it if it still exists.
    """
    source_id, book_ref_id = existing_source_and_bookref

    payload = {
        "quote_text": "Test quote text (pytest)",
        "source_id": source_id,
        "book_ref_id": book_ref_id,  # can be None; schema allows it
    }

    resp = client.post(BASE, json=payload)
    assert resp.status_code == 200, resp.text

    data = resp.json()
    assert isinstance(data, dict)
    assert "id" in data
    assert data["quote_text"] == payload["quote_text"]
    assert data["source_id"] == source_id
    # book_ref_id may be None; only assert if we provided one
    if book_ref_id is not None:
        assert data["book_ref_id"] == book_ref_id

    quote_id = data["id"]
    assert isinstance(quote_id, int)
    assert quote_id > 0

    yield quote_id

    # Cleanup attempt (best-effort)
    client.delete(f"{BASE}/{quote_id}")


def test_list_quotes_returns_list():
    resp = client.get(BASE)
    assert resp.status_code == 200, resp.text

    data = resp.json()
    assert isinstance(data, list)
    # list can be empty; still valid


def test_create_quote_validation_error(existing_source_and_bookref):
    source_id, book_ref_id = existing_source_and_bookref

    # Empty quote_text should fail validation (min_length=1, if you set it)
    payload = {
        "quote_text": "",
        "source_id": source_id,
        "book_ref_id": book_ref_id,
    }

    resp = client.post(BASE, json=payload)
    assert resp.status_code in (422, 400), resp.text
    # 422 if Pydantic validation triggers; 400 if you validate manually in router


def test_get_quote_by_id(created_quote_id):
    resp = client.get(f"{BASE}/{created_quote_id}")
    assert resp.status_code == 200, resp.text

    data = resp.json()
    assert isinstance(data, dict)
    assert data["id"] == created_quote_id
    assert "quote_text" in data
    assert "source_id" in data
    assert "source_name" in data  # because your SELECT joins source


def test_list_quotes_contains_created_quote(created_quote_id):
    resp = client.get(BASE)
    assert resp.status_code == 200, resp.text

    data = resp.json()
    assert isinstance(data, list)

    ids = [row.get("id") for row in data if isinstance(row, dict)]
    assert created_quote_id in ids


def test_delete_quote_then_404(created_quote_id):
    # Delete should succeed
    del_resp = client.delete(f"{BASE}/{created_quote_id}")
    assert del_resp.status_code == 204, del_resp.text
    assert del_resp.content in (b"", None) or del_resp.text == ""

    # Afterwards, GET should 404
    get_resp = client.get(f"{BASE}/{created_quote_id}")
    assert get_resp.status_code == 404, get_resp.text

    body = get_resp.json()
    assert isinstance(body, dict)
    assert "detail" in body


def test_delete_nonexistent_quote_404():
    # Use a very large ID unlikely to exist
    quote_id = 999999999

    resp = client.delete(f"{BASE}/{quote_id}")
    assert resp.status_code == 404, resp.text

    body = resp.json()
    assert isinstance(body, dict)
    assert body.get("detail") in ("Quote not found",) or "not found" in str(body.get("detail", "")).lower()
