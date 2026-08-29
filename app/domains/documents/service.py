from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Document
from app.domains.documents.repository import DocumentRepository
from app.schemas.document import DocumentCreate


class DocumentService:
    """Logic for documents."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = DocumentRepository(session)

    async def create(self, data: DocumentCreate) -> Document:
        """Create a document and commit the transaction."""
        document = await self._repository.create(data)
        await self._session.commit()

        return document

    async def list_all(self) -> Sequence[Document]:
        """Return all documents."""
        return await self._repository.list_all()
