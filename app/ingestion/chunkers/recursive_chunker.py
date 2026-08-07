from uuid import uuid4

from app.ingestion.chunkers.base import BaseChunker
from app.models.chunk import Chunk
from app.models.metadata import ChunkMetadata


class RecursiveChunker(BaseChunker):
    """Splits text into overlapping chunks."""

    def __init__(
        self,
        document_id: str,
        source: str | None = None,
        chunk_size: int = 800,
        overlap: int = 150,
    ):
        self.document_id = document_id
        self.source = source or document_id
        self.chunk_size = chunk_size
        self.overlap = overlap

    def split(
        self,
        text: str,
        page_number: int | None = None,
    ) -> list[Chunk]:
        chunks: list[Chunk] = []
        page_number = 0 if page_number is None else page_number

        start = 0
        index = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))

            chunk_text = text[start:end]

            chunks.append(
                Chunk(
                    chunk_id=str(uuid4()),
                    document_id=self.document_id,
                    chunk_index=index,
                    text=chunk_text,
                    metadata=ChunkMetadata(
                        source=self.source,
                        page_number=page_number,
                        chunk_index=index,
                        start_char=start,
                        end_char=min(end, len(text)),
                    ),
                )
            )

            if end == len(text):
                break

            start += self.chunk_size - self.overlap
            index += 1

        return chunks
