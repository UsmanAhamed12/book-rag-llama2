from pathlib import Path

from app.llm.service import LLMService
from app.rag.prompt import SYSTEM_PROMPT
from app.retrieval.models import RetrievalResult
from app.retrieval.retriever import Retriever
from app.services.chat_memory_service import ChatMemoryService


class RAGPipeline:
    """Build grounded answers from the most relevant book chunks."""

    # Chroma uses L2 distance for this collection. With normalized embeddings,
    # this removes clearly unrelated chunks while retaining useful matches.
    minimum_context_score = 0.35

    def __init__(
        self,
        retriever: Retriever,
        llm: LLMService,
        memory: ChatMemoryService,
    ) -> None:
        self.retriever = retriever
        self.llm = llm
        self.memory = memory

    def build_prompt(
        self,
        session_id: int,
        question: str,
        top_k: int = 5,
    ) -> tuple[str, list[RetrievalResult]]:
        results = self.retriever.search(question, top_k)
        grounded_results = [
            result for result in results if result.score >= self.minimum_context_score
        ]
        history = self.build_history(session_id)

        context_parts = []
        for index, result in enumerate(grounded_results, start=1):
            metadata = result.metadata
            source = self._source_name(result)
            page = metadata.get("page_number", result.page_number)
            chunk = metadata.get("chunk_index", 0)
            context_parts.append(
                f"""[S{index}] File: {source} | Page: {page} | Chunk: {chunk}
<document_text>
{result.text}
</document_text>"""
            )

        context = "\n\n".join(context_parts) or "No relevant book context was found."

        return (
            SYSTEM_PROMPT.format(
                history=history,
                context=context,
                question=question,
            ),
            grounded_results,
        )

    def ask(self, session_id: int, question: str) -> dict:
        self.memory.save_message(session_id=session_id, role="user", message=question)

        prompt, results = self.build_prompt(session_id=session_id, question=question)
        answer = (
            self.llm.answer(prompt)
            if results
            else "I cannot find this information in the provided book context."
        )

        self.memory.save_message(
            session_id=session_id,
            role="assistant",
            message=answer,
        )

        return {
            "answer": answer,
            "sources": self._build_sources(results),
        }

    @staticmethod
    def _source_name(result: RetrievalResult) -> str:
        return Path(str(result.metadata.get("source") or result.document_id)).name

    @classmethod
    def _build_sources(cls, results: list[RetrievalResult]) -> list[dict]:
        """Return only citations for chunks actually supplied to the LLM."""
        sources: list[dict] = []
        seen: set[tuple[str, int, int]] = set()

        for index, result in enumerate(results, start=1):
            metadata = result.metadata
            source = cls._source_name(result)
            page_number = int(metadata.get("page_number", result.page_number))
            chunk_number = int(metadata.get("chunk_index", 0))
            identity = (source, page_number, chunk_number)
            if identity in seen:
                continue

            seen.add(identity)
            sources.append(
                {
                    "reference": f"S{index}",
                    "file_name": source,
                    "page_number": page_number,
                    "chunk_number": chunk_number,
                    "score": round(result.score, 4),
                }
            )

        return sources

    def build_history(self, session_id: int) -> str:
        # A bounded history leaves the model enough room for the retrieved book
        # context, which is the authoritative evidence for the answer.
        messages = self.memory.get_messages(session_id)[-8:]
        return "\n".join(f"{message.role}: {message.message}" for message in messages)
