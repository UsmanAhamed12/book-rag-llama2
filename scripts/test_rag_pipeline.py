from app.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider,
)
from app.llm.service import LLMService
from app.retrieval.retriever import Retriever
from app.rag.pipeline import RAGPipeline

embedding = SentenceTransformerProvider()

retriever = Retriever(embedding)

llm = LLMService()

rag = RAGPipeline(
    retriever,
    llm,
)

question = "What is data engineering?"

answer = rag.ask(question)

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(answer)