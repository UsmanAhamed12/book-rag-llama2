from app.db.chroma import get_chroma_client
from app.embeddings.base import BaseEmbeddingProvider
from app.retrieval.models import RetrievalResult


class Retriever:
    def __init__(
        self,
        embedding_provider: BaseEmbeddingProvider,
        collection_name: str = "book_chunks",
    ) -> None:
        self.embedding_provider = embedding_provider

        client = get_chroma_client()

        self.collection = client.get_or_create_collection(
            name=collection_name,
        )

    def search(
        self,
        query: str,
        user_id: int,
        document_ids: list[str] | None = None,
        top_k: int = 10,
        score_threshold: float | None = None,
    ) -> list[RetrievalResult]:

        where_filter: dict = {
        "user_id": user_id,
    }

        if document_ids:
            where_filter = {
                "$and": [
                    {
                        "user_id": user_id,
                    },
                    {
                        "document_id": {
                            "$in": document_ids,
                        },
                    },
                ],
            }
        query_embedding = self.embedding_provider.embed([query])[0]



        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=where_filter,
        )

        documents = results.get("documents", [[]])[0]
        distances = results.get("distances", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        output: list[RetrievalResult] = []

        for text, distance, metadata in zip(
            documents,
            distances,
            metadatas,
            strict=True,
        ):
            similarity = 1 / (1 + float(distance))

            output.append(
                RetrievalResult(
                    text=text,
                    score=similarity,
                    metadata=metadata,
                    document_id=metadata["document_id"],
                    page_number=metadata["page_number"],
                )
            )

        if score_threshold is not None:
            output = [
                result
                for result in output
                if result.score >= score_threshold
            ]

        output.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return output

