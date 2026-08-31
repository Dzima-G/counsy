from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Document
from app.schemas.document import DocumentCreate


class DocumentRepository:
    """Data access for document entities."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, data: DocumentCreate) -> Document:
        """Create a new document in the database."""
        document = Document(
            title=data.title,
            source=data.source,
            content=data.content,
            doc_type=data.doc_type,
        )
        self._session.add(document)
        await self._session.flush()

        return document

    async def list_all(self) -> Sequence[Document]:
        """List all documents in the database."""
        result = await self._session.execute(select(Document))

        return result.scalars().all()

    async def get_by_id(self, document_id: UUID) -> Document | None:
        """Return a document by id or None if not found."""
        result = await self._session.execute(
            select(Document).where(Document.id == document_id),
        )

        return result.scalars().one_or_none()
