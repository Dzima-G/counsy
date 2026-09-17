from collections.abc import Sequence
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Document
from app.domains.documents.repository import DocumentRepository
from app.schemas.document import DocumentCreate
from app.workers.tasks import process_document


class DocumentService:
    """Logic for documents."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._repository = DocumentRepository(session)

    async def create(self, data: DocumentCreate) -> Document:
        """Create a document and commit the transaction."""
        document = await self._repository.create(data)
        await self._session.commit()

        process_document.delay(str(document.id))

        return document

    async def list_all(self) -> Sequence[Document]:
        """Return all documents."""
        return await self._repository.list_all()

    async def get_by_id(self, document_id: UUID) -> Document | None:
        """Return a document by id or None if not found."""
        return await self._repository.get_by_id(document_id)
