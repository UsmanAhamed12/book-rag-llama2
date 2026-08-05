from app.db.postgres import engine, Base

from app.models.database.document import DocumentDB
from app.models.database.chat import ChatHistory


Base.metadata.create_all(
    bind=engine
)


print("Tables created")