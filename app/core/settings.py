from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""

    app_name: str = "Book RAG"

    app_version: str = "0.1.0"

    environment: str = "development"

    log_level: str = "INFO"

    ollama_model: str = "llama3.2"

    chroma_db_path: str = "data/chroma"

    embedding_model: str = "BAAI/bge-small-en-v1.5"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    book_path: str = "data/uploads/Data_Engineering.pdf"

    chroma_path: str = "data/chroma"

    # class Config:
    #     env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
