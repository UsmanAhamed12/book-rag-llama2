from app.embeddings.embedding_service import EmbeddingService
from app.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider,
)


def test_embedding_generation():
    provider = SentenceTransformerProvider()

    service = EmbeddingService(provider)

    vectors = service.embed_chunks([])

    assert vectors == []
