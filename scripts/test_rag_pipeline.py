from app.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider,
)

from app.retrieval.retriever import Retriever
from app.rag.pipeline import RAGPipeline


embedding = SentenceTransformerProvider()


retriever = Retriever(
    embedding
)


rag = RAGPipeline(
    retriever
)


prompt = rag.build_prompt(
    "What is data engineering?"
)


print(prompt)