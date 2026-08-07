from app.embeddings.base import BaseEmbeddingProvider
from app.db.chroma import get_chroma_client
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
            name=collection_name
        )


    def search(
        self,
        query: str,
        top_k: int = 10,
        score_threshold: float = 0.80
    ) -> list[RetrievalResult]:


        query_embedding = (
            self.embedding_provider
            .embed([query])[0]
        )


        results = self.collection.query(

            query_embeddings=[
                query_embedding
            ],

            n_results=top_k,

        )


        documents = results["documents"][0]

        distances = results["distances"][0]

        metadatas = results["metadatas"][0]


        output: list[RetrievalResult] = []

        for text, distance, metadata in zip(
            documents,
            distances,
            metadatas,
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

        filtered = [
            result
            for result in output
            if result.score <= score_threshold
        ]

        filtered.sort(key=lambda x: x.score)

        return filtered