import pytest

from app.evaluation.metrics import evaluate_retrieval
from app.evaluation.models import RetrievalExample
from app.retrieval.models import RetrievalResult


def result(document_id: str, page: int, chunk: int) -> RetrievalResult:
    return RetrievalResult(
        text="text",
        score=0.9,
        metadata={"chunk_index": chunk},
        document_id=document_id,
        page_number=page,
    )


def test_evaluate_retrieval_computes_hit_recall_and_mrr() -> None:
    examples = [
        RetrievalExample(
            question="q1",
            relevant_chunks=frozenset({("doc-1", 1, 0)}),
        ),
        RetrievalExample(
            question="q2",
            relevant_chunks=frozenset({("doc-2", 3, 2), ("doc-2", 4, 0)}),
        ),
    ]

    ranked_results = [
        [result("noise", 9, 0), result("doc-1", 1, 0)],
        [result("doc-2", 3, 2), result("noise", 1, 0)],
    ]

    metrics = evaluate_retrieval(examples, ranked_results, k=2)

    assert metrics.examples == 2
    assert metrics.hit_rate_at_k == pytest.approx(1.0)
    assert metrics.recall_at_k == pytest.approx(0.75)
    assert metrics.mean_reciprocal_rank == pytest.approx(0.75)


def test_evaluate_retrieval_rejects_invalid_k() -> None:
    with pytest.raises(ValueError, match="k must be greater than zero"):
        evaluate_retrieval([], [], k=0)


def test_evaluate_retrieval_rejects_mismatched_inputs() -> None:
    example = RetrievalExample(question="q", relevant_chunks=frozenset())

    with pytest.raises(ValueError, match="same length"):
        evaluate_retrieval([example], [], k=5)
