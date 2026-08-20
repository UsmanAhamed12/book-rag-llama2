# app/embeddings/sentence_transformer_provider.py

from typing import cast

from sentence_transformers import SentenceTransformer

from app.embeddings.base import BaseEmbeddingProvider


class SentenceTransformerProvider(BaseEmbeddingProvider):
    """SentenceTransformer embedding provider."""

    query_instruction = "Represent this sentence for searching relevant passages: "

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
    ) -> None:
        self.model = SentenceTransformer(model_name)

    def embed(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return cast(
            list[list[float]],
            embeddings.tolist(),
        )

    def embed_query(self, query: str) -> list[float]:
        """Apply the BGE retrieval instruction to query embeddings only."""
        return self.embed([f"{self.query_instruction}{query.strip()}"])[0]
