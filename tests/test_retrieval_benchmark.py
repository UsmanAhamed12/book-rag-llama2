from app.evaluation.benchmark import RetrievalBenchmark
from app.evaluation.models import RetrievalExample
from app.retrieval.models import RetrievalResult


class DummyRetriever:
    def search(
        self,
        query: str,
        user_id: int,
        document_ids: list[str] | None = None,
        top_k: int = 5,
    ) -> list[RetrievalResult]:
        del query, user_id, document_ids, top_k
        return [
            RetrievalResult(
                text="relevant chunk",
                score=0.95,
                metadata={"chunk_index": 2},
                document_id="doc-1",
                page_number=3,
            )
        ]


def test_benchmark_runs_retrieval_and_returns_metrics() -> None:
    benchmark = RetrievalBenchmark(
        retriever=DummyRetriever(),  # type: ignore[arg-type]
        user_id=1,
        top_k=5,
    )

    examples = [
        RetrievalExample(
            question="What is data engineering?",
            relevant_chunks=frozenset({("doc-1", 3, 2)}),
        )
    ]

    result = benchmark.run(examples)

    assert result.examples == 1
    assert result.hit_rate_at_k == 1.0
    assert result.recall_at_k == 1.0
    assert result.mean_reciprocal_rank == 1.0


def test_benchmark_rejects_invalid_top_k() -> None:
    try:
        RetrievalBenchmark(
            retriever=DummyRetriever(),  # type: ignore[arg-type]
            user_id=1,
            top_k=0,
        )
    except ValueError as exc:
        assert str(exc) == "top_k must be greater than zero"
    else:
        raise AssertionError("Expected ValueError")
