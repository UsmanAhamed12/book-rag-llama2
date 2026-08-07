from abc import ABC, abstractmethod


class BaseEmbeddingProvider(ABC):
    """Base interface for embedding providers."""

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Generate embeddings for a list of texts."""
        raise NotImplementedError
