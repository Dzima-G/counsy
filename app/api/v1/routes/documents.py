from collections.abc import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.session import get_db_session
from app.domains.documents.service import DocumentService
from app.schemas.document import DocumentCreate, DocumentRead

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post(path="", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
async def create_document(data: DocumentCreate, session: AsyncSession = Depends(get_db_session)) -> DocumentRead:
    """Upload a new document."""
    service = DocumentService(session)
    document = await service.create(data)

    return DocumentRead.model_validate(document)


@router.get(path="", response_model=list[DocumentRead])
async def list_documents(
    session: AsyncSession = Depends(get_db_session),
) -> Sequence[DocumentRead]:
    """List all documents."""
    service = DocumentService(session)
    documents = await service.list_all()

    return [DocumentRead.model_validate(doc) for doc in documents]


@router.get(path="/{document_id}", response_model=DocumentRead)
async def get_document(
    document_id: UUID,
    session: AsyncSession = Depends(get_db_session),
) -> DocumentRead:
    """Get document by id."""
    service = DocumentService(session)
    document = await service.get_by_id(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return DocumentRead.model_validate(document)
