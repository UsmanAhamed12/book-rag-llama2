from datetime import datetime

from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.postgres import Base


class DocumentDB(Base):

    __tablename__ = "documents"


    id: Mapped[int] = mapped_column(
        primary_key=True
    )


    filename: Mapped[str] = mapped_column(
        String(255)
    )


    chunks: Mapped[int] = mapped_column(
        Integer
    )


    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )