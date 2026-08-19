from dataclasses import dataclass

from app.evaluation.models import RetrievalExample, result_identity
from app.retrieval.models import RetrievalResult


@dataclass(frozen=True)
class RankedDiagnosticResult:
    rank: int
    document_id: str
    page_number: int
    chunk_index: int
    score: float
    is_relevant: bool


@dataclass(frozen=True)
class RetrievalDiagnostic:
    question: str
    expected_chunks: tuple[tuple[str, int, int], ...]
    first_relevant_rank: int | None
    retrieved: tuple[RankedDiagnosticResult, ...]


def build_retrieval_diagnostic(
    example: RetrievalExample,
    results: list[RetrievalResult],
    k: int,
) -> RetrievalDiagnostic:
    if k <= 0:
        raise ValueError("k must be greater than zero")

    ranked: list[RankedDiagnosticResult] = []
    first_relevant_rank: int | None = None

    for rank, result in enumerate(results[:k], start=1):
        document_id, page_number, chunk_index = result_identity(result)
        identity = (document_id, page_number, chunk_index)
        is_relevant = identity in example.relevant_chunks

        if is_relevant and first_relevant_rank is None:
            first_relevant_rank = rank

        ranked.append(
            RankedDiagnosticResult(
                rank=rank,
                document_id=document_id,
                page_number=page_number,
                chunk_index=chunk_index,
                score=result.score,
                is_relevant=is_relevant,
            )
        )

    return RetrievalDiagnostic(
        question=example.question,
        expected_chunks=tuple(sorted(example.relevant_chunks)),
        first_relevant_rank=first_relevant_rank,
        retrieved=tuple(ranked),
    )
