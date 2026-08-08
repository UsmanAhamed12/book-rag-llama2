from app.db.postgres import Base, engine


from app.models.database.document import DocumentDB
from app.models.database.user import UserDB
from app.models.database.chat import ChatHistory
from app.models.database.chat_session import ChatSessionDB
from app.models.database.chat_message import ChatMessageDB


Base.metadata.create_all(
    bind=engine
)

print("Tables created")


