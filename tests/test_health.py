from http import HTTPStatus

from httpx import AsyncClient


async def test_health(client: AsyncClient) -> None:
    response = await client.get("/api/v1/health")

    body = response.json()

    assert response.status_code == HTTPStatus.OK, f"Expected status 200, received: {response.status_code}."
    assert body == {"status": "ok"}, f"Invalid response body: {body}."
