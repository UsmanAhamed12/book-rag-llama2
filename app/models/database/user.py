from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.postgres import Base


class UserDB(Base):
    __tablename__ = "users"

    def __init__(
        self,
        email: str,
        password_hash: str | None = None,
        hashed_password: str | None = None,
    ) -> None:
        super().__init__()

        resolved_password_hash = password_hash or hashed_password
        if resolved_password_hash is None:
            raise ValueError("A password hash is required")

        self.email = email
        self.hashed_password = resolved_password_hash

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )
