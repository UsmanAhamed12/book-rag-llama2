from uuid import uuid4

from app.ingestion.chunkers.base import BaseChunker
from app.models.chunk import Chunk
from app.models.metadata import ChunkMetadata


class RecursiveChunker(BaseChunker):
    def __init__(
        self,
        document_id: str,
        chunk_size: int = 800,
        overlap: int = 150,
    ):
        self.document_id = document_id
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(self, text: str) -> list[Chunk]:
        chunks: list[Chunk] = []

        start = 0
        index = 0

        while start < len(text):
            end = start + self.chunk_size

            chunk_text = text[start:end]

            chunks.append(
                Chunk(
                    chunk_id=str(uuid4()),
                    document_id=self.document_id,
                    chunk_index=index,
                    text=chunk_text,
                    metadata=ChunkMetadata(
    source=self.document_id,
    chunk_index=index,
    start_char=start,
    end_char=min(end, len(text)),
),
                )
            )

            index += 1
            start += self.chunk_size - self.overlap

        return chunks
