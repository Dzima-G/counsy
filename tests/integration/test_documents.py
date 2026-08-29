from http import HTTPStatus

from httpx import AsyncClient


async def test_create_document(client: AsyncClient) -> None:
    """Checks document creation."""
    payload = {
        "title": "Contract №1",
        "source": "docs/contracts/Contract №1.pdf",
        "content": "This is a test document...",
        "doc_type": "contract",
    }

    response = await client.post("/api/v1/documents", json=payload)
    body = response.json()

    assert response.status_code == HTTPStatus.CREATED, f"Expected status 201, received: {response.status_code}."
    assert body["title"] == payload["title"], f"Expected {payload['title']}, received {body['title']}."
    assert body["doc_type"] == payload["doc_type"], f"Expected {payload['doc_type']}, received {body['doc_type']}"
    assert body["id"] is not None, f"Expected id, received {body['id']}."
    assert body["created_at"] is not None, f"Expected created_at, received {body['created_at']}."


async def test_get_list_document(client: AsyncClient) -> None:
    """Checks document list."""
    payload = {
        "title": "Regulation № 1-A",
        "source": "/docs/reg/Regulation № 1-A .pdf",
        "content": "Regulation text...",
        "doc_type": "regulation",
    }
    await client.post("/api/v1/documents", json=payload)

    response = await client.get("/api/v1/documents")
    body = response.json()

    assert response.status_code == HTTPStatus.OK
    assert len(body) == 1
    assert body[0]["title"] == "Regulation № 1-A"
