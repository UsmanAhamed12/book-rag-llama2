from collections.abc import Sequence

from app.evaluation.models import (
    RetrievalEvaluation,
    RetrievalExample,
    result_identity,
)
from app.retrieval.models import RetrievalResult


def hit_at_k(
    example: RetrievalExample,
    results: Sequence[RetrievalResult],
    k: int,
) -> float:
    retrieved = {result_identity(result) for result in results[:k]}
    return float(bool(retrieved & example.relevant_chunks))


def recall_at_k(
    example: RetrievalExample,
    results: Sequence[RetrievalResult],
    k: int,
) -> float:
    if not example.relevant_chunks:
        return 0.0

    retrieved = {result_identity(result) for result in results[:k]}
    relevant_retrieved = retrieved & example.relevant_chunks
    return len(relevant_retrieved) / len(example.relevant_chunks)


def reciprocal_rank(
    example: RetrievalExample,
    results: Sequence[RetrievalResult],
    k: int,
) -> float:
    for rank, result in enumerate(results[:k], start=1):
        if result_identity(result) in example.relevant_chunks:
            return 1.0 / rank

    return 0.0


def evaluate_retrieval(
    examples: Sequence[RetrievalExample],
    ranked_results: Sequence[Sequence[RetrievalResult]],
    k: int,
) -> RetrievalEvaluation:
    if k <= 0:
        raise ValueError("k must be greater than zero")

    if len(examples) != len(ranked_results):
        raise ValueError("examples and ranked_results must have the same length")

    if not examples:
        return RetrievalEvaluation(
            examples=0,
            hit_rate_at_k=0.0,
            recall_at_k=0.0,
            mean_reciprocal_rank=0.0,
        )

    hits = [hit_at_k(example, results, k) for example, results in zip(examples, ranked_results, strict=True)]
    recalls = [recall_at_k(example, results, k) for example, results in zip(examples, ranked_results, strict=True)]
    reciprocal_ranks = [
        reciprocal_rank(example, results, k)
        for example, results in zip(examples, ranked_results, strict=True)
    ]

    count = len(examples)

    return RetrievalEvaluation(
        examples=count,
        hit_rate_at_k=sum(hits) / count,
        recall_at_k=sum(recalls) / count,
        mean_reciprocal_rank=sum(reciprocal_ranks) / count,
    )
