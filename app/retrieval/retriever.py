from app.db.chroma import get_chroma_client
from app.embeddings.base import BaseEmbeddingProvider
from app.retrieval.models import RetrievalResult


class Retriever:

    def __init__(
        self,
        embedding_provider: BaseEmbeddingProvider,
        collection_name: str = "book_chunks",
    ) -> None:

        client = get_chroma_client()

        self.collection = client.get_collection(
            collection_name
        )

        self.embedding_provider = embedding_provider


    def search(
        self,
        query: str,
        top_k: int = 8,
    ) -> list[RetrievalResult]:

        query_embedding = (
            self.embedding_provider.embed(
                [query]
            )[0]
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


        return [
            RetrievalResult(
                text=document,
                score=distance,
                metadata=metadata,
            )
            for document, distance, metadata
            in zip(
                documents,
                distances,
                metadatas,
            )
        ]