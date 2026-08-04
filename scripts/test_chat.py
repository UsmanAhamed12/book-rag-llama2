from app.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider,
)

from app.retrieval.retriever import Retriever
from app.rag.pipeline import RAGPipeline
from app.llm.service import LLMService


embedding = SentenceTransformerProvider()


retriever = Retriever(
    embedding
)


llm = LLMService()


rag = RAGPipeline(
    retriever,
    llm,
)


answer = rag.ask(
    "What is data?"
)


print(answer)