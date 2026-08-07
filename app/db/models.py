from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    String,
)

from app.db.postgres import Base


class DocumentModel(Base):
    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    filename = Column(
        String,
        nullable=False,
    )

    file_path = Column(
        String,
        nullable=False,
    )

    status = Column(
        String,
        default="processing",
    )

    chunk_count = Column(
        Integer,
        default=0,
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow,
    )
