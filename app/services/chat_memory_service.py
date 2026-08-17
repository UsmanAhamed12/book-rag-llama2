from datetime import datetime

from sqlalchemy.orm import Session

from app.models.database.chat_message import ChatMessageDB
from app.models.database.chat_session import ChatSessionDB


class ChatMemoryService:
    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def create_session(
        self,
        user_id: int,
    ) -> ChatSessionDB:

        session = ChatSessionDB(
            user_id=user_id,
            title="New Chat",
        )

        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def get_session(
        self,
        session_id: int,
        user_id: int,
    ) -> ChatSessionDB | None:

        return (
            self.db.query(ChatSessionDB)
            .filter(
                ChatSessionDB.id == session_id,
                ChatSessionDB.user_id == user_id,
            )
            .first()
        )

    def save_message(
        self,
        session_id: int,
        user_id: int,
        role: str,
        message: str,
        sources: list[dict] | None = None,
    ) -> None:

        session = self.get_session(
            session_id=session_id,
            user_id=user_id,
        )

        if session is None:
            raise ValueError("Chat session not found.")

        chat = ChatMessageDB(
            session_id=session_id,
            role=role,
            message=message,
            sources=sources,
        )

        self.db.add(chat)
        self.db.commit()

    def get_messages(
        self,
        session_id: int,
        user_id: int,
    ) -> list[ChatMessageDB]:

        session = self.get_session(
            session_id=session_id,
            user_id=user_id,
        )

        if session is None:
            raise ValueError("Chat session not found.")

        return (
            self.db.query(ChatMessageDB)
            .filter(
                ChatMessageDB.session_id == session_id,
            )
            .order_by(ChatMessageDB.id)
            .all()
        )

    def rename_session(
        self,
        session_id: int,
        user_id: int,
        title: str,
    ) -> ChatSessionDB | None:
        session = self.get_session(
            session_id=session_id,
            user_id=user_id,
        )

        if session is None:
            return None

        session.title = title.strip()
        session.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(session)

        return session


    def delete_session(
        self,
        session_id: int,
        user_id: int,
    ) -> bool:
        session = self.get_session(
            session_id=session_id,
            user_id=user_id,
        )

        if session is None:
            return False

        (
            self.db.query(ChatMessageDB)
            .filter(
                ChatMessageDB.session_id == session_id,
            )
            .delete()
        )

        self.db.delete(session)
        self.db.commit()

        return True