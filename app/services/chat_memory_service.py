from sqlalchemy.orm import Session

from app.models.database.chat_session import ChatSessionDB
from app.models.database.chat_message import ChatMessageDB


class ChatMemoryService:

    def __init__(
        self,
        db: Session,
    ) -> None:

        self.db = db

    def create_session(
        self,
    ) -> ChatSessionDB:

        session = ChatSessionDB()

        self.db.add(session)

        self.db.commit()

        self.db.refresh(session)

        return session

    def save_message(
        self,
        session_id: int,
        role: str,
        message: str,
    ) -> None:

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
    ) -> list[ChatMessageDB]:

        return (
            self.db.query(ChatMessageDB)
            .filter(
                ChatMessageDB.session_id == session_id
            )
            .order_by(
                ChatMessageDB.id
            )
            .all()
        )