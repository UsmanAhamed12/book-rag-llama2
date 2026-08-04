from abc import ABC, abstractmethod

from app.models.chunk import Chunk


class BaseChunker(ABC):
    """Base interface for all chunkers."""

    @abstractmethod
    def split(self, text: str) -> list[Chunk]:
        """Split text into chunks."""
        raise NotImplementedError
