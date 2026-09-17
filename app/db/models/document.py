from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import DateTime, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.chunk import Chunk


class Document(Base):
    """Source document (contract, regulation, instruction) the assistant answers from."""

    __tablename__ = "documents"

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        server_default=func.uuidv7(),
    )
    doc_status: Mapped[str] = mapped_column(String(20), server_default="pending")
    title: Mapped[str] = mapped_column(String(255))
    source: Mapped[str] = mapped_column(String(512))
    content: Mapped[str] = mapped_column(Text)
    doc_type: Mapped[str] = mapped_column(String(50))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")
