from app.db.postgres import engine, Base

from app.models.database.document import DocumentDB
from app.models.database.chat_session import ChatSessionDB
from app.models.database.chat_message import ChatMessageDB
from app.models.database.user import UserDB

Base.metadata.create_all(bind=engine)

print("Tables created")