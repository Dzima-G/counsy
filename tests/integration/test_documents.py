from http import HTTPStatus
from uuid import uuid4

from httpx import AsyncClient


async def test_create_document(client: AsyncClient) -> None:
    """Checks document upload."""
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
    assert body["doc_status"] == "pending", f"Expected pending, received {body['doc_status']}."


async def test_get_list_document(client: AsyncClient) -> None:
    """Checks document list."""
    payloads = [
        {
            "title": "Regulation № 1-A",
            "source": "/docs/reg/Regulation № 1-A .pdf",
            "content": "Regulation text...",
            "doc_type": "regulation",
        },
        {
            "title": "Contract №1",
            "source": "docs/contracts/Contract №1.pdf",
            "content": "This is a test document...",
            "doc_type": "contract",
        },
    ]

    for payload in payloads:
        await client.post("/api/v1/documents", json=payload)

    response = await client.get("/api/v1/documents")
    body = response.json()

    assert response.status_code == HTTPStatus.OK, f"Expected status 200, received: {response.status_code}."
    assert len(body) == 2, f"Expected 2 document, received {len(body)}."


async def test_list_documents_empty(client: AsyncClient) -> None:
    """Checks empty list."""
    response = await client.get("/api/v1/documents")
    assert response.status_code == HTTPStatus.OK, f"Expected status 200, received: {response.status_code}."
    assert response.json() == [], f"Expected empty list, received {response.json()}."


async def test_get_document(client: AsyncClient) -> None:
    """Checks get document by id."""
    payload = {
        "title": "Contract №1",
        "source": "docs/contracts/1.pdf",
        "content": "text...",
        "doc_type": "contract",
    }

    created = await client.post("/api/v1/documents", json=payload)
    document_id = created.json()["id"]

    response = await client.get(f"/api/v1/documents/{document_id}")
    body = response.json()

    assert response.status_code == HTTPStatus.OK, f"Expected status 200, received: {response.status_code}."
    assert body["id"] == document_id, f"Expected {document_id}, received {body['id']}."
    assert body["title"] == payload["title"], f"Expected {payload['title']}, received {body['title']}."


async def test_get_document_not_found(client: AsyncClient) -> None:
    """Checks 404 for a missing document."""
    missing_id = uuid4()

    response = await client.get(f"/api/v1/documents/{missing_id}")

    assert response.status_code == HTTPStatus.NOT_FOUND, f"Expected status 404, received: {response.status_code}."
