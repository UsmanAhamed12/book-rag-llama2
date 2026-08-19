from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol


class RerankableResult(Protocol):
    text: str


class CrossEncoderLike(Protocol):
    def predict(self, sentences: list[tuple[str, str]]) -> Sequence[float]: ...


@dataclass(frozen=True)
class RerankedResult:
    result: RerankableResult
    rerank_score: float
    original_rank: int


class CrossEncoderReranker:
    """Rerank retrieved candidates using query-document relevance scores."""

    def __init__(self, model: CrossEncoderLike) -> None:
        self._model = model

    def rerank(
        self,
        *,
        query: str,
        results: Sequence[RerankableResult],
        top_k: int,
    ) -> list[RerankedResult]:
        if not query.strip():
            raise ValueError("query must not be empty")

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")

        if not results:
            return []

        pairs = [(query, result.text) for result in results]
        scores = self._model.predict(pairs)

        if len(scores) != len(results):
            raise ValueError(
                "reranker returned a different number of scores than candidates"
            )

        reranked = [
            RerankedResult(
                result=result,
                rerank_score=float(score),
                original_rank=rank,
            )
            for rank, (result, score) in enumerate(
                zip(results, scores, strict=True),
                start=1,
            )
        ]

        reranked.sort(key=lambda item: (-item.rerank_score, item.original_rank))

        return reranked[:top_k]
