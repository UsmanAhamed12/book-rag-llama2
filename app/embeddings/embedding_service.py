from app.embeddings.base import BaseEmbeddingProvider
from app.models.chunk import Chunk


class EmbeddingService:
    def __init__(
        self,
        provider: BaseEmbeddingProvider,
    ) -> None:
        self.provider = provider

    def embed_chunks(
        self,
        chunks: list[Chunk],
    ) -> list[list[float]]:
        texts = [chunk.text for chunk in chunks]

        return self.provider.embed(texts)
