from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = "Book RAG Assistant"
    app_version: str = "1.0.0"
    environment: str = "development"
    log_level: str = "INFO"

    # Authentication
    secret_key: str = "development-only-change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    # PostgreSQL
    postgres_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/book_rag"

    # Ollama
    ollama_model: str = "llama3.2"
    ollama_host: str = "http://localhost:11434"

    # Embeddings
    embedding_model: str = "BAAI/bge-small-en-v1.5"

    # Retrieval / reranking
    reranking_enabled: bool = False
    reranker_model: str = "cross-encoder/ms-marco-MiniLM-L6-v2"
    retrieval_candidate_k: int = 10
    retrieval_top_k: int = 5

    # Storage
    chroma_db_path: str = "data/chroma"
    chroma_path: str = "data/chroma"
    upload_dir: str = "data/uploads"

    # Legacy/default document configuration
    book_path: str = "data/uploads/Data_Engineering.pdf"
    document_id: str = "data_engineering_book"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
