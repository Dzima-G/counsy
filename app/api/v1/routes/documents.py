from collections.abc import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.db.session import get_db_session
from app.domains.documents.service import DocumentService
from app.schemas.document import DocumentCreate, DocumentRead

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post(path="", response_model=DocumentRead, status_code=status.HTTP_201_CREATED)
async def create_document(data: DocumentCreate, session: AsyncSession = Depends(get_db_session)) -> DocumentRead:
    """Create a new document."""
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
