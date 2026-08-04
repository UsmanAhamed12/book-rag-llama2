from app.embeddings.embedding_service import EmbeddingService
from app.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider,
)

provider = SentenceTransformerProvider()

service = EmbeddingService(provider)

vectors = service.provider.embed(
    [
        "What is data engineering?",
        "Python is a programming language.",
    ]
)

print(len(vectors))
print(len(vectors[0]))