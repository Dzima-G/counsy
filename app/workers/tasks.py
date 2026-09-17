import asyncio
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Chunk, Document
from app.db.session import session_scope
from app.domains.documents.chunker import split_text
from app.schemas.document import DocumentStatus
from app.workers.celery_app import celery_app


@celery_app.task
def ping() -> str:
    return "pong"


@celery_app.task
def process_document(document_id: str) -> None:
    """Celery task entry point: run document processing in the background."""
    asyncio.run(_process_document(UUID(document_id)))


async def _process_document(document_id: UUID) -> None:
    """Load the document, run chunk processing, and mark it failed on error."""
    async with session_scope() as session:
        document = await session.get(Document, document_id)
        if document is None:
            return

        try:
            await _build_chunks(session, document)
        except Exception:
            await session.rollback()
            document.doc_status = DocumentStatus.FAILED
            await session.commit()
            raise


async def _build_chunks(session: AsyncSession, document: Document) -> None:
    """Split the document into chunks, persist them, and mark it ready."""
    document.doc_status = DocumentStatus.PROCESSING
    await session.commit()

    pieces = split_text(document.content)
    for index, piece in enumerate(pieces):
        session.add(Chunk(document_id=document.id, content=piece, chunk_index=index))

    document.doc_status = DocumentStatus.READY
    await session.commit()
