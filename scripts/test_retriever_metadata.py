from app.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider
)

from app.retrieval.retriever import Retriever


embedding = SentenceTransformerProvider()


retriever = Retriever(
    embedding
)


results = retriever.search(
    "What is data visualization?"
)


for result in results:

    print("----------------")

    print(result.text[:200])

    print(result.score)

    print(result.metadata)