import pytest
from fastapi.testclient import TestClient
import psycopg2.extras

from main import app
from db import get_conn  # adjust if your get_conn lives elsewhere

client = TestClient(app)

BASE = "/api/insight-quotes"   # change if your prefix differs


def _get_existing_insight_and_quote():
    """
    Returns (insight_id, quote_id) from the DB if they exist.
    Skips tests if missing, because we don’t know your insight/quote POST endpoints here.
    """
    with get_conn() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id FROM insight ORDER BY id ASC LIMIT 1;")
            insight = cur.fetchone()

            cur.execute("SELECT id FROM quote ORDER BY id ASC LIMIT 1;")
            quote = cur.fetchone()

    if not insight or not quote:
        return None, None

    return insight["id"], quote["id"]


@pytest.fixture()
def existing_insight_and_quote():
    insight_id, quote_id = _get_existing_insight_and_quote()
    if insight_id is None or quote_id is None:
        pytest.skip("Need at least 1 insight row and 1 quote row in DB to run insight_quote tests.")
    assert isinstance(insight_id, int)
    assert isinstance(quote_id, int)
    return insight_id, quote_id


def _detach_if_exists(insight_id: int, quote_id: int):
    """Best-effort cleanup."""
    client.delete(f"{BASE}?insight_id={insight_id}&quote_id={quote_id}")


@pytest.fixture()
def created_link(existing_insight_and_quote):
    """
    Creates an insight_quote link via API and yields:
      (insight_quote_id, insight_id, quote_id)

    Always cleans up by detaching at the end.
    """
    insight_id, quote_id = existing_insight_and_quote

    # Ensure clean slate (avoid UNIQUE(insight_id, quote_id) conflicts)
    _detach_if_exists(insight_id, quote_id)

    payload = {
        "insight_id": insight_id,
        "quote_id": quote_id,
        "note": "pytest note",
    }

    res = client.post(BASE, json=payload)

    # If your API returns 409 when already exists, we already detached above, so 201 expected.
    assert res.status_code in (200, 201), res.text

    data = res.json()
    assert isinstance(data, dict)

    assert "id" in data
    assert data["insight_id"] == insight_id
    assert data["quote_id"] == quote_id
    assert data.get("note") == "pytest note"

    insight_quote_id = data["id"]
    assert isinstance(insight_quote_id, int)
    assert insight_quote_id > 0

    yield insight_quote_id, insight_id, quote_id

    # cleanup
    _detach_if_exists(insight_id, quote_id)


def test_attach_quote_to_insight(created_link):
    insight_quote_id, insight_id, quote_id = created_link
    assert isinstance(insight_quote_id, int)
    assert isinstance(insight_id, int)
    assert isinstance(quote_id, int)


def test_get_link_by_id(created_link):
    insight_quote_id, insight_id, quote_id = created_link

    res = client.get(f"{BASE}/{insight_quote_id}")
    assert res.status_code == 200, res.text

    data = res.json()
    assert isinstance(data, dict)
    assert data["id"] == insight_quote_id
    assert data["insight_id"] == insight_id
    assert data["quote_id"] == quote_id
    assert "note" in data


def test_list_links_by_insight(created_link):
    insight_quote_id, insight_id, quote_id = created_link

    res = client.get(f"{BASE}?insight_id={insight_id}")
    assert res.status_code == 200, res.text

    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    ids = [row.get("id") for row in data if isinstance(row, dict)]
    assert insight_quote_id in ids


def test_list_links_by_quote(created_link):
    insight_quote_id, insight_id, quote_id = created_link

    res = client.get(f"{BASE}?quote_id={quote_id}")
    assert res.status_code == 200, res.text

    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    ids = [row.get("id") for row in data if isinstance(row, dict)]
    assert insight_quote_id in ids


def test_list_links_by_pair_returns_0_or_1(created_link):
    insight_quote_id, insight_id, quote_id = created_link

    res = client.get(f"{BASE}?insight_id={insight_id}&quote_id={quote_id}")
    assert res.status_code == 200, res.text

    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["id"] == insight_quote_id


def test_get_quotes_for_insight_view(created_link):
    _, insight_id, _ = created_link

    res = client.get(f"{BASE}/insight/{insight_id}/quotes")
    assert res.status_code == 200, res.text

    data = res.json()
    assert isinstance(data, list)

    # If the insight has at least the one link we created, list should be non-empty.
    assert len(data) >= 1

    row = data[0]
    assert isinstance(row, dict)

    # Your QuoteForInsightOut fields
    assert "quote_id" in row
    assert "quote_text" in row
    assert "source_id" in row
    assert "source_name" in row
    # optional book ref fields may be None
    assert "page_start" in row
    assert "chapter_start" in row


def test_get_insights_for_quote_rich_view(created_link):
    _, _, quote_id = created_link

    res = client.get(f"{BASE}/quote/{quote_id}/insights")
    assert res.status_code == 200, res.text

    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    row = data[0]
    assert isinstance(row, dict)

    # Join-table fields
    assert "insight_quote_id" in row
    assert "insight_quote_note" in row

    # Your INSIGHT_SELECT_BASE fields should be present (some may be null due to LEFT JOIN)
    assert "id" in row                      # insight id
    assert "insight_content" in row
    assert "created_at" in row
    assert "updated_at" in row

    assert "insight_creator_id" in row
    assert "insight_creator_name" in row

    assert "source_id" in row
    assert "source_name" in row

    assert "source_creator_id" in row
    assert "source_creator_name" in row

    assert "source_type_id" in row
    assert "source_type_name" in row


def test_detach_then_pair_returns_empty(existing_insight_and_quote):
    insight_id, quote_id = existing_insight_and_quote

    # Ensure link exists (create it)
    _detach_if_exists(insight_id, quote_id)
    create_res = client.post(BASE, json={"insight_id": insight_id, "quote_id": quote_id, "note": "pytest"})
    assert create_res.status_code in (200, 201), create_res.text

    # Detach
    del_res = client.delete(f"{BASE}?insight_id={insight_id}&quote_id={quote_id}")
    assert del_res.status_code == 204, del_res.text
    assert del_res.content == b""

    # Now pair query should return empty list
    res = client.get(f"{BASE}?insight_id={insight_id}&quote_id={quote_id}")
    assert res.status_code == 200, res.text
    data = res.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_detach_nonexistent_returns_404(existing_insight_and_quote):
    insight_id, quote_id = existing_insight_and_quote

    # Ensure it does not exist
    _detach_if_exists(insight_id, quote_id)

    del_res = client.delete(f"{BASE}?insight_id={insight_id}&quote_id={quote_id}")
    assert del_res.status_code == 404, del_res.text
    body = del_res.json()
    assert isinstance(body, dict)
    assert "detail" in body
