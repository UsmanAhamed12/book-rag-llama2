from app.embeddings.sentence_transformer_provider import (
    SentenceTransformerProvider,
)
from app.llm.service import LLMService
from app.rag.pipeline import RAGPipeline
from app.retrieval.retriever import Retriever

embedding = SentenceTransformerProvider()

retriever = Retriever(embedding)

llm = LLMService()

rag = RAGPipeline(
    retriever,
    llm,
)

question = "What is data engineering?"

response = rag.ask(question)

print(response["answer"])

print("\nSources")

for source in response["sources"]:
    print(f"Document: {source.document_id} | Page: {source.page_number}")

print("\nQuestion:")
print(question)

print("\nAnswer:")
print(response["answer"])
