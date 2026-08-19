from dataclasses import dataclass

from app.retrieval.models import RetrievalResult


@dataclass(frozen=True)
class RetrievalExample:
    """One labeled retrieval question and its relevant chunk identities."""

    question: str
    relevant_chunks: frozenset[tuple[str, int, int]]


@dataclass(frozen=True)
class RetrievalEvaluation:
    """Aggregate deterministic retrieval metrics."""

    examples: int
    hit_rate_at_k: float
    recall_at_k: float
    mean_reciprocal_rank: float


def result_identity(result: RetrievalResult) -> tuple[str, int, int]:
    raw_chunk_index = result.metadata.get("chunk_index", 0)

    if isinstance(raw_chunk_index, bool):
        chunk_index = int(raw_chunk_index)
    elif isinstance(raw_chunk_index, (int, float)):
        chunk_index = int(raw_chunk_index)
    elif isinstance(raw_chunk_index, str):
        try:
            chunk_index = int(raw_chunk_index)
        except ValueError:
            chunk_index = 0
    else:
        chunk_index = 0

    return result.document_id, result.page_number, chunk_index
