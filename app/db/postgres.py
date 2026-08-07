from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.settings import settings

engine = create_engine(
    settings.postgres_url,
    echo=False,
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


def ensure_schema() -> None:
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())

    if "documents" not in existing_tables:
        Base.metadata.create_all(bind=engine)
        return

    existing_columns = inspector.get_columns("documents")
    column_names = {column["name"] for column in existing_columns}

    if "file_size" not in column_names:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE documents ADD COLUMN file_size INTEGER DEFAULT 0")
            )

    if "page_count" not in column_names:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE documents ADD COLUMN page_count INTEGER DEFAULT 0")
            )

    if "chunks" not in column_names:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE documents ADD COLUMN chunks INTEGER DEFAULT 0")
            )

    if "status" not in column_names:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE documents ADD COLUMN status VARCHAR(50) "
                    "DEFAULT 'processing'"
                )
            )

    if "created_at" not in column_names:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE documents ADD COLUMN created_at TIMESTAMP "
                    "DEFAULT CURRENT_TIMESTAMP"
                )
            )

    if "updated_at" not in column_names:
        with engine.begin() as connection:
            connection.execute(
                text(
                    "ALTER TABLE documents ADD COLUMN updated_at TIMESTAMP "
                    "DEFAULT CURRENT_TIMESTAMP"
                )
            )


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
