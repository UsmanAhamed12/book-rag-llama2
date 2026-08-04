from app.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider,
)

from app.retrieval.retriever import Retriever


provider = SentenceTransformerProvider()


retriever = Retriever(
    provider
)


results = retriever.search(
    "What is data engineering?",
    top_k=3,
)


for result in results:

    print("=" * 50)

    print(
        result.text[:500]
    )

    print(
        "Score:",
        result.score
    )