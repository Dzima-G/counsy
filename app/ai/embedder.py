import httpx

from app.core.config import settings


async def embed_texts(texts: list[str]) -> list[list[float]]:
    """Return embedding vectors for the given texts (via the TEI service)."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            url=f"{settings.embedder.url}/embed",
            json={"inputs": texts},
        )
        response.raise_for_status()

        return response.json()
