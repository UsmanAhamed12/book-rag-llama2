from app.core.settings import Settings


def test_database_url_prefers_explicit_postgres_url() -> None:
    settings = Settings(
        postgres_url="postgresql+psycopg://explicit:test@db:5432/example"
    )

    assert settings.database_url == "postgresql+psycopg://explicit:test@db:5432/example"


def test_database_url_builds_from_components() -> None:
    settings = Settings(
        postgres_url=None,
        postgres_host="database.internal",
        postgres_port=5432,
        postgres_db="book_rag",
        postgres_user="bookrag_admin",
        postgres_password="secret-value",
    )

    assert settings.database_url == (
        "postgresql+psycopg://"
        "bookrag_admin:secret-value"
        "@database.internal:5432/book_rag"
    )


def test_database_url_escapes_credentials() -> None:
    settings = Settings(
        postgres_url=None,
        postgres_user="user@example.com",
        postgres_password="p@ss/word",
    )

    assert "user%40example.com" in settings.database_url
    assert "p%40ss%2Fword" in settings.database_url
