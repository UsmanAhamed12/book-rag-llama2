from collections.abc import Mapping, Sequence
from typing import Any

from app.retrieval.models import RetrievalResult
from app.retrieval.retriever import Retriever


class DocumentScopedEvaluationRetriever:
    """Retrieve legacy chunks by document ID for offline evaluation only.

    Production retrieval continues to enforce user filtering. This adapter exists
    only for historical Chroma collections whose metadata predates ``user_id``.
    """

    def __init__(self, retriever: Retriever) -> None:
        self.embedding_provider = retriever.embedding_provider
        self.collection = retriever.collection

    @staticmethod
    def _to_int(value: object, default: int = 0) -> int:
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, int):
            return value
        if isinstance(value, float):
            return int(value)
        if isinstance(value, str):
            try:
                return int(value)
            except ValueError:
                return default
        return default

    @staticmethod
    def _metadata_dict(metadata: Mapping[str, Any] | None) -> dict[str, Any]:
        if metadata is None:
            return {}
        return dict(metadata)

    @staticmethod
    def _first_or_empty[T](value: list[list[T]] | None) -> list[T]:
        if not value:
            return []
        return value[0]

    def search(
        self,
        query: str,
        user_id: int,
        document_ids: list[str] | None = None,
        top_k: int = 10,
        score_threshold: float | None = None,
    ) -> list[RetrievalResult]:
        del user_id

        if not document_ids:
            raise ValueError("document_ids are required for legacy evaluation")

        where_filter: dict[str, Any]
        if len(document_ids) == 1:
            where_filter = {"document_id": document_ids[0]}
        else:
            where_filter = {"document_id": {"$in": document_ids}}

        query_embedding = self.embedding_provider.embed([query])[0]
        normalized_query: list[Sequence[float]] = [query_embedding]

        results = self.collection.query(
            query_embeddings=normalized_query,
            n_results=top_k,
            where=where_filter,
        )

        documents = self._first_or_empty(results.get("documents"))
        distances = self._first_or_empty(results.get("distances"))
        metadatas = self._first_or_empty(results.get("metadatas"))

        output: list[RetrievalResult] = []

        for text, distance, raw_metadata in zip(
            documents,
            distances,
            metadatas,
            strict=True,
        ):
            metadata = self._metadata_dict(raw_metadata)
            similarity = 1 / (1 + float(distance))

            if score_threshold is not None and similarity < score_threshold:
                continue

            output.append(
                RetrievalResult(
                    text=text,
                    score=similarity,
                    metadata=metadata,
                    document_id=str(metadata.get("document_id", "")),
                    page_number=self._to_int(metadata.get("page_number", 0)),
                )
            )

        output.sort(
            key=lambda result: result.score,
            reverse=True,
        )
        return output
