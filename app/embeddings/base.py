from abc import ABC, abstractmethod


class BaseEmbeddingProvider(ABC):
    """Base interface for embedding providers."""

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts."""
        raise NotImplementedError

    def embed_query(self, query: str) -> list[float]:
        """Generate an embedding optimized for document retrieval."""
        return self.embed([query])[0]
