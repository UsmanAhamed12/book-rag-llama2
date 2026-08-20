from app.embeddings.base import BaseEmbeddingProvider
from app.embeddings.embedding_service import EmbeddingService


class FakeEmbeddingProvider(BaseEmbeddingProvider):
    def embed(self, texts: list[str]) -> list[list[float]]:
        return [[0.0] for _ in texts]


def test_embedding_generation() -> None:
    service = EmbeddingService(FakeEmbeddingProvider())

    vectors = service.embed_chunks([])

    assert vectors == []
