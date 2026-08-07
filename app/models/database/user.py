from datetime import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.postgres import Base


class UserDB(Base):
    __tablename__ = "users"

    def __init__(
        self,
        email: str,
        password_hash: str | None = None,
        hashed_password: str | None = None,
        **kwargs,
    ) -> None:
        kwargs.setdefault("email", email)

        if password_hash is not None:
            kwargs["hashed_password"] = password_hash
        elif hashed_password is not None:
            kwargs["hashed_password"] = hashed_password

        super().__init__(**kwargs)

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

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