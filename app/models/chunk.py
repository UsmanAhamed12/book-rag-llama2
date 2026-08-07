from dataclasses import dataclass

from app.models.metadata import ChunkMetadata


@dataclass(slots=True)
class Chunk:
    """Represents one chunk of a document."""

    chunk_id: str
    document_id: str
    chunk_index: int
    text: str
    metadata: ChunkMetadata
