from uuid import UUID

from pydantic import BaseModel


class SearchQuery(BaseModel):
    """Search Query."""

    question: str


class SearchResult(BaseModel):
    """Search Result."""

    content: str
    """Chunk content."""
    title: str
    """Document title."""
    source: str
    """Document source."""
    document_id: UUID
    """Document ID."""
