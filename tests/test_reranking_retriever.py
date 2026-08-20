from collections.abc import Sequence

import pytest

from app.retrieval.models import RetrievalResult
from app.retrieval.reranking_retriever import RerankingRetriever
from app.retrieval.retriever import Retriever


class FakeBaseRetriever(Retriever):
    def __init__(self, results: list[RetrievalResult]) -> None:
        self.results = results
        self.search_top_k: int | None = None

    def search(
        self,
        query: str,
        user_id: int,
        document_ids: list[str] | None = None,
        top_k: int = 10,
        score_threshold: float | None = None,
    ) -> list[RetrievalResult]:
        del query, user_id, document_ids, score_threshold
        self.search_top_k = top_k
        return self.results[:top_k]

    def search_balanced(
        self,
        query: str,
        user_id: int,
        document_ids: list[str],
        per_document_k: int = 4,
        score_threshold: float | None = None,
    ) -> list[RetrievalResult]:
        del query, user_id, document_ids, per_document_k, score_threshold
        return self.results

    def get_representative_chunks(
        self,
        user_id: int,
        document_id: str,
        sample_count: int = 6,
    ) -> list[RetrievalResult]:
        del user_id, document_id, sample_count
        return self.results

    def search_for_summary(
        self,
        query: str,
        user_id: int,
        document_ids: list[str],
        semantic_k: int = 4,
        representative_k: int = 6,
    ) -> list[RetrievalResult]:
        del query, user_id, document_ids, semantic_k, representative_k
        return self.results


class FakeReranker:
    def __init__(self, scores: Sequence[float]) -> None:
        self.scores = scores
        self.received_pairs: list[tuple[str, str]] = []

    def predict(self, sentences: list[tuple[str, str]]) -> Sequence[float]:
        self.received_pairs = sentences
        return self.scores


def make_result(text: str, score: float) -> RetrievalResult:
    return RetrievalResult(
        text=text,
        score=score,
        metadata={"chunk_index": 0},
        document_id="9",
        page_number=1,
    )


def test_reranking_retriever_reranks_vector_candidates() -> None:
    results = [
        make_result("first", 0.9),
        make_result("second", 0.8),
        make_result("third", 0.7),
    ]
    base = FakeBaseRetriever(results)
    reranker = FakeReranker([0.1, 0.9, 0.5])
    retriever = RerankingRetriever(base, reranker, candidate_k=3)

    reranked = retriever.search(
        query="question",
        user_id=1,
        document_ids=["9"],
        top_k=2,
    )

    assert [result.text for result in reranked] == ["second", "third"]
    assert reranked[0].score == pytest.approx(0.94)
    assert reranked[1].score == pytest.approx(0.56)
    assert base.search_top_k == 3
    assert reranker.received_pairs == [
        ("question", "first"),
        ("question", "second"),
        ("question", "third"),
    ]


def test_reranking_retriever_uses_top_k_when_larger_than_candidate_k() -> None:
    results = [
        make_result("first", 0.9),
        make_result("second", 0.8),
        make_result("third", 0.7),
    ]
    base = FakeBaseRetriever(results)
    retriever = RerankingRetriever(
        base,
        FakeReranker([0.3, 0.2, 0.1]),
        candidate_k=2,
    )

    retriever.search(query="question", user_id=1, top_k=3)

    assert base.search_top_k == 3


def test_reranking_retriever_returns_empty_without_candidates() -> None:
    retriever = RerankingRetriever(
        FakeBaseRetriever([]),
        FakeReranker([]),
    )

    assert retriever.search(query="question", user_id=1, top_k=5) == []


def test_reranking_retriever_rejects_invalid_candidate_k() -> None:
    with pytest.raises(ValueError, match="candidate_k"):
        RerankingRetriever(
            FakeBaseRetriever([]),
            FakeReranker([]),
            candidate_k=0,
        )


def test_reranking_retriever_rejects_invalid_weight() -> None:
    with pytest.raises(ValueError, match="reranker_weight"):
        RerankingRetriever(
            FakeBaseRetriever([]),
            FakeReranker([]),
            reranker_weight=1.1,
        )


def test_reranking_retriever_rejects_invalid_top_k() -> None:
    retriever = RerankingRetriever(
        FakeBaseRetriever([]),
        FakeReranker([]),
    )

    with pytest.raises(ValueError, match="top_k"):
        retriever.search(query="question", user_id=1, top_k=0)


def test_reranking_retriever_rejects_score_count_mismatch() -> None:
    results = [make_result("first", 0.9), make_result("second", 0.8)]
    retriever = RerankingRetriever(
        FakeBaseRetriever(results),
        FakeReranker([0.5]),
    )

    with pytest.raises(ValueError, match="different number"):
        retriever.search(query="question", user_id=1, top_k=2)
