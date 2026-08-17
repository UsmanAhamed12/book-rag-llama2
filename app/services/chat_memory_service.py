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