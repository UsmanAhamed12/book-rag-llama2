from dataclasses import dataclass

import pytest

from app.evaluation.reranker import CrossEncoderReranker


@dataclass
class FakeResult:
    text: str


class FakeCrossEncoder:
    def __init__(self, scores: list[float]) -> None:
        self.scores = scores
        self.received_pairs: list[tuple[str, str]] = []

    def predict(self, sentences: list[tuple[str, str]]) -> list[float]:
        self.received_pairs = sentences
        return self.scores


def test_reranker_orders_results_by_cross_encoder_score() -> None:
    results = [
        FakeResult("first"),
        FakeResult("second"),
        FakeResult("third"),
    ]

    model = FakeCrossEncoder([0.2, 0.9, 0.5])
    reranker = CrossEncoderReranker(model)

    reranked = reranker.rerank(
        query="test question",
        results=results,
        top_k=3,
    )

    assert [item.result.text for item in reranked] == [
        "second",
        "third",
        "first",
    ]
    assert [item.original_rank for item in reranked] == [2, 3, 1]

    assert model.received_pairs == [
        ("test question", "first"),
        ("test question", "second"),
        ("test question", "third"),
    ]


def test_reranker_respects_top_k() -> None:
    results = [
        FakeResult("first"),
        FakeResult("second"),
        FakeResult("third"),
    ]

    reranker = CrossEncoderReranker(FakeCrossEncoder([0.1, 0.8, 0.5]))

    reranked = reranker.rerank(
        query="question",
        results=results,
        top_k=2,
    )

    assert len(reranked) == 2
    assert [item.result.text for item in reranked] == [
        "second",
        "third",
    ]


def test_reranker_returns_empty_list_for_no_candidates() -> None:
    reranker = CrossEncoderReranker(FakeCrossEncoder([]))

    assert (
        reranker.rerank(
            query="question",
            results=[],
            top_k=5,
        )
        == []
    )


def test_reranker_rejects_empty_query() -> None:
    reranker = CrossEncoderReranker(FakeCrossEncoder([]))

    with pytest.raises(ValueError, match="query"):
        reranker.rerank(
            query="   ",
            results=[],
            top_k=5,
        )


def test_reranker_rejects_invalid_top_k() -> None:
    reranker = CrossEncoderReranker(FakeCrossEncoder([]))

    with pytest.raises(ValueError, match="top_k"):
        reranker.rerank(
            query="question",
            results=[],
            top_k=0,
        )


def test_reranker_rejects_score_count_mismatch() -> None:
    results = [
        FakeResult("first"),
        FakeResult("second"),
    ]

    reranker = CrossEncoderReranker(FakeCrossEncoder([0.5]))

    with pytest.raises(ValueError, match="different number"):
        reranker.rerank(
            query="question",
            results=results,
            top_k=2,
        )
