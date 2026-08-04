from dataclasses import dataclass


@dataclass(slots=True)
class ChunkMetadata:
    source: str
    chunk_index: int
    start_char: int
    end_char: int