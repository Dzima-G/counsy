from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.ai.embedder import embed_texts
from app.core.config import SEARCH_TOP_K
from app.db.models import Chunk
from app.domains.documents.repository import ChunkRepository


class SearchService:
    """Semantic search over document chunks."""

    def __init__(self, session: AsyncSession) -> None:
        self._repository = ChunkRepository(session)

    async def search(self, question: str, limit: int = SEARCH_TOP_K) -> Sequence[Chunk]:
        """Return the chunks most relevant to the question."""
        query_vector = (await embed_texts([f"query: {question}"]))[0]
        chunks = await self._repository.search_similar(query_vector, limit)

        return chunks
