from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.domains.documents.search import SearchService
from app.schemas.search import SearchQuery, SearchResult

router = APIRouter(prefix="/search", tags=["search"])


@router.post("", response_model=list[SearchResult])
async def search(data: SearchQuery, session: AsyncSession = Depends(get_db_session)) -> list[SearchResult]:
    """Return the chunks most relevant to the question."""
    service = SearchService(session)
    chunks = await service.search(data.question)

    return [
        SearchResult(
            content=chunk.content,
            title=chunk.document.title,
            source=chunk.document.source,
            document_id=chunk.document_id,
        )
        for chunk in chunks
    ]
