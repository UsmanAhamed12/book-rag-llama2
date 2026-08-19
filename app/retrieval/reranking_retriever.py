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
    ) -> None:
        if candidate_k <= 0:
            raise ValueError("candidate_k must be greater than zero")

        self.base_retriever = base_retriever
        self.reranker = reranker
        self.candidate_k = candidate_k

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

        ranked = sorted(
            zip(candidates, scores, strict=True),
            key=lambda item: float(item[1]),
            reverse=True,
        )

        return [candidate for candidate, _ in ranked[:top_k]]

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
