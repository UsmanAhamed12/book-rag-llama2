from app.core.settings import settings
from app.embeddings.embedding_service import EmbeddingService
from app.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider,
)
from app.services.ingestion_service import IngestionService
from app.vectorstores.chroma_store import ChromaVectorStore


provider = SentenceTransformerProvider()


embedding_service = EmbeddingService(
    provider
)


vector_store = ChromaVectorStore()


service = IngestionService(
    embedding_service,
    vector_store,
)


count = service.ingest(
    settings.book_path
)


print(
    f"Indexed chunks: {count}"
)