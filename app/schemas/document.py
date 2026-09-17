from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DocumentType(StrEnum):
    """Document type."""

    CONTRACT = "contract"
    REGULATION = "regulation"
    NORMATIVE = "normative"
    INSTRUCTION = "instruction"
    OTHER = "other"


class DocumentStatus(StrEnum):
    """Document status."""

    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class DocumentCreate(BaseModel):
    """Input data for creating a document."""

    title: str
    """Document name."""
    source: str
    """Document source."""
    content: str
    """Document content."""
    doc_type: DocumentType
    """Document type."""


class DocumentRead(BaseModel):
    """Data returned when reading a document."""

    id: UUID
    """Document id."""
    doc_status: DocumentStatus
    """Document status."""
    title: str
    """Document name."""
    source: str
    """Document source."""
    content: str
    """Document content."""
    doc_type: DocumentType
    """Document type."""
    created_at: datetime
    """Document creation date."""
    updated_at: datetime
    """Document creation time."""

    model_config = ConfigDict(from_attributes=True)
