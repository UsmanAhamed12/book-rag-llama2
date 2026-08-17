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

    def search_balanced(
        self,
        query: str,
        user_id: int,
        document_ids: list[str],
        per_document_k: int = 4,
        score_threshold: float | None = None,
    ) -> list[RetrievalResult]:
        query_embedding = self.embedding_provider.embed([query])[0]

        output: list[RetrievalResult] = []

        for document_id in document_ids:
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=per_document_k,
                where={
                    "$and": [
                        {
                            "user_id": user_id,
                        },
                        {
                            "document_id": document_id,
                        },
                    ],
                },
            )

            documents = results.get(
                "documents",
                [[]],
            )[0]

            distances = results.get(
                "distances",
                [[]],
            )[0]

            metadatas = results.get(
                "metadatas",
                [[]],
            )[0]

            for text, distance, metadata in zip(
                documents,
                distances,
                metadatas,
                strict=True,
            ):
                similarity = 1 / (
                    1 + float(distance)
                )

                if (
                    score_threshold is not None
                    and similarity < score_threshold
                ):
                    continue

                output.append(
                    RetrievalResult(
                        text=text,
                        score=similarity,
                        metadata=metadata,
                        document_id=metadata[
                            "document_id"
                        ],
                        page_number=metadata[
                            "page_number"
                        ],
                    )
                )

        output.sort(
            key=lambda result: result.score,
            reverse=True,
        )

        return output

    def get_representative_chunks(
        self,
        user_id: int,
        document_id: str,
        sample_count: int = 6,
    ) -> list[RetrievalResult]:
        results = self.collection.get(
            where={
                "$and": [
                    {
                        "user_id": user_id,
                    },
                    {
                        "document_id": document_id,
                    },
                ],
            },
            include=[
                "documents",
                "metadatas",
            ],
        )

        documents = results.get(
            "documents",
            [],
        )

        metadatas = results.get(
            "metadatas",
            [],
        )

        if not documents:
            return []

        indexed = list(
            zip(
                documents,
                metadatas,
                strict=True,
            )
        )

        indexed.sort(
            key=lambda item: (
                int(
                    item[1].get(
                        "page_number",
                        0,
                    )
                ),
                int(
                    item[1].get(
                        "chunk_index",
                        0,
                    )
                ),
            )
        )

        if len(indexed) <= sample_count:
            selected = indexed
        else:
            positions = [
                round(
                    index
                    * (len(indexed) - 1)
                    / (sample_count - 1)
                )
                for index in range(
                    sample_count
                )
            ]

            selected = [
                indexed[position]
                for position in positions
            ]

        return [
            RetrievalResult(
                text=text,
                score=1.0,
                metadata=metadata,
                document_id=str(
                    metadata[
                        "document_id"
                    ]
                ),
                page_number=int(
                    metadata[
                        "page_number"
                    ]
                ),
            )
            for text, metadata in selected
        ]

    def search_for_summary(
        self,
        query: str,
        user_id: int,
        document_ids: list[str],
        semantic_k: int = 4,
        representative_k: int = 6,
    ) -> list[RetrievalResult]:
        combined: list[RetrievalResult] = []

        for document_id in document_ids:
            semantic_results = self.search(
                query=query,
                user_id=user_id,
                document_ids=[
                    document_id
                ],
                top_k=semantic_k,
            )

            representative_results = (
                self.get_representative_chunks(
                    user_id=user_id,
                    document_id=document_id,
                    sample_count=representative_k,
                )
            )

            seen: set[
                tuple[str, int, int]
            ] = set()

            for result in (
                representative_results
                + semantic_results
            ):
                identity = (
                    result.document_id,
                    result.page_number,
                    int(
                        result.metadata.get(
                            "chunk_index",
                            0,
                        )
                    ),
                )

                if identity in seen:
                    continue

                seen.add(identity)
                combined.append(result)

        return combined

