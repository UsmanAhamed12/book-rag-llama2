from collections.abc import Sequence
from typing import Protocol

from app.retrieval.models import RetrievalResult
from app.retrieval.retriever import Retriever


class CrossEncoderLike(Protocol):
    def predict(self, sentences: list[tuple[str, str]]) -> Sequence[float]: ...


class RerankingRetriever(Retriever):
    """Wrap vector retrieval with an optional cross-encoder ranking stage."""

    def __init__(
        self,
        base_retriever: Retriever,
        reranker: CrossEncoderLike,
        candidate_k: int = 20,
        reranker_weight: float = 0.7,
    ) -> None:
        if candidate_k <= 0:
            raise ValueError("candidate_k must be greater than zero")
        if not 0.0 <= reranker_weight <= 1.0:
            raise ValueError("reranker_weight must be between zero and one")

        self.base_retriever = base_retriever
        self.reranker = reranker
        self.candidate_k = candidate_k
        self.reranker_weight = reranker_weight

    @staticmethod
    def _normalize_scores(scores: Sequence[float]) -> list[float]:
        numeric_scores = [float(score) for score in scores]
        minimum = min(numeric_scores)
        maximum = max(numeric_scores)

        if maximum == minimum:
            return [0.5 for _ in numeric_scores]

        score_range = maximum - minimum
        return [(score - minimum) / score_range for score in numeric_scores]

    def search(
        self,
        query: str,
        user_id: int,
        document_ids: list[str] | None = None,
        top_k: int = 10,
        score_threshold: float | None = None,
    ) -> list[RetrievalResult]:
        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")

        candidates = self.base_retriever.search(
            query=query,
            user_id=user_id,
            document_ids=document_ids,
            top_k=max(self.candidate_k, top_k),
            score_threshold=score_threshold,
        )

        if not candidates:
            return []

        pairs = [(query, candidate.text) for candidate in candidates]
        scores = self.reranker.predict(pairs)

        if len(scores) != len(candidates):
            raise ValueError(
                "reranker returned a different number of scores than candidates"
            )

        normalized_reranker_scores = self._normalize_scores(scores)
        vector_weight = 1.0 - self.reranker_weight

        for candidate, reranker_score in zip(
            candidates,
            normalized_reranker_scores,
            strict=True,
        ):
            candidate.score = (
                self.reranker_weight * reranker_score + vector_weight * candidate.score
            )

        ranked = sorted(
            candidates,
            key=lambda candidate: candidate.score,
            reverse=True,
        )

        return ranked[:top_k]

    def search_balanced(
        self,
        query: str,
        user_id: int,
        document_ids: list[str],
        per_document_k: int = 4,
        score_threshold: float | None = None,
    ) -> list[RetrievalResult]:
        return self.base_retriever.search_balanced(
            query=query,
            user_id=user_id,
            document_ids=document_ids,
            per_document_k=per_document_k,
            score_threshold=score_threshold,
        )

    def get_representative_chunks(
        self,
        user_id: int,
        document_id: str,
        sample_count: int = 6,
    ) -> list[RetrievalResult]:
        return self.base_retriever.get_representative_chunks(
            user_id=user_id,
            document_id=document_id,
            sample_count=sample_count,
        )

    def search_for_summary(
        self,
        query: str,
        user_id: int,
        document_ids: list[str],
        semantic_k: int = 4,
        representative_k: int = 6,
    ) -> list[RetrievalResult]:
        return self.base_retriever.search_for_summary(
            query=query,
            user_id=user_id,
            document_ids=document_ids,
            semantic_k=semantic_k,
            representative_k=representative_k,
        )
