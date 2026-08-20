from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context
from app.core.settings import settings
from app.db.postgres import Base
from app.models.database.chat import ChatHistory  # noqa: F401
from app.models.database.chat_message import ChatMessageDB  # noqa: F401
from app.models.database.chat_session import ChatSessionDB  # noqa: F401
from app.models.database.document import DocumentDB  # noqa: F401
from app.models.database.user import UserDB  # noqa: F401

# Import all models so SQLAlchemy metadata knows about them.

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


# Use the same database URL as the application.
config.set_main_option(
    "sqlalchemy.url",
    settings.database_url.replace("%", "%%"),
)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in offline mode."""

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in online mode."""

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
