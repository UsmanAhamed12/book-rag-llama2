from pathlib import Path

from app.llm.service import LLMService
from app.rag.prompt import SYSTEM_PROMPT
from app.retrieval.models import RetrievalResult
from app.retrieval.retriever import Retriever
from app.services.chat_memory_service import ChatMemoryService


class RAGPipeline:
    """Build grounded answers from the most relevant book chunks."""

    minimum_context_score = 0.35

    def __init__(
        self,
        retriever: Retriever,
        llm: LLMService
    ) -> None:
        self.retriever = retriever
        self.llm = llm

    def build_prompt(
        self,
        session_id: int,
        user_id: int,
        question: str,
        memory: ChatMemoryService,
        top_k: int = 5,
        document_ids: list[int] | None = None,
    ) -> tuple[str, list[RetrievalResult]]:
        history = self.build_history(
            session_id=session_id,
            user_id=user_id,
            memory=memory,
        )

        retrieval_history = self.build_retrieval_context(
            session_id=session_id,
            user_id=user_id,
            memory=memory,
        )

        retrieval_query = self.llm.rewrite_query(
            question=question,
            history=retrieval_history,
        )

        results = self.retriever.search(
            retrieval_query,
            user_id=user_id,
            document_ids=(
                [
                    str(document_id)
                    for document_id in document_ids
                ]
                if document_ids
                else None
            ),
            top_k=top_k,
        )

        grounded_results = [
            result
            for result in results
            if result.score >= self.minimum_context_score
        ]

        context_parts: list[str] = []

        for index, result in enumerate(
            grounded_results,
            start=1,
        ):
            metadata = result.metadata

            source = self._source_name(
                result,
            )

            page = metadata.get(
                "page_number",
                result.page_number,
            )

            chunk = metadata.get(
                "chunk_index",
                0,
            )

            context_parts.append(
                f"""[S{index}] File: {source} | Page: {page} | Chunk: {chunk}
    <document_text>
    {result.text}
    </document_text>"""
            )

        context = (
            "\n\n".join(context_parts)
            if context_parts
            else "No relevant book context was found."
        )

        prompt = SYSTEM_PROMPT.format(
            history=history,
            context=context,
            question=question,
        )

        return prompt, grounded_results

    def build_retrieval_context(
        self,
        session_id: int,
        user_id: int,
        memory: ChatMemoryService,
    ) -> str:
        messages = memory.get_messages(
            session_id=session_id,
            user_id=user_id,
        )

        user_messages = [
            message.message
            for message in messages
            if message.role == "user"
        ]

        return "\n".join(user_messages[-3:])

    def ask(
        self,
        session_id: int,
        user_id: int,
        question: str,
        memory: ChatMemoryService,
        document_ids: list[int] | None = None,
    ) -> dict:
        prompt, results = self.build_prompt(
            session_id=session_id,
            user_id=user_id,
            question=question,
            memory=memory,
            document_ids=document_ids,
        )

        answer = (
            self.llm.answer(prompt)
            if results
            else "I cannot find this information in the provided book context."
        )

        sources = self._build_sources(results)

        memory.save_message(
            session_id=session_id,
            user_id=user_id,
            role="user",
            message=question,
        )

        memory.save_message(
            session_id=session_id,
            user_id=user_id,
            role="assistant",
            message=answer,
            sources=sources,
        )

        return {
            "answer": answer,
            "sources": sources,
        }

    @staticmethod
    def _source_name(result: RetrievalResult) -> str:
        return Path(
            str(
                result.metadata.get(
                    "source",
                )
                or result.document_id
            )
        ).name

    @classmethod
    def _build_sources(
        cls,
        results: list[RetrievalResult],
    ) -> list[dict]:
        """Return only citations for chunks supplied to the LLM."""

        sources: list[dict] = []

        seen: set[tuple[str, int, int]] = set()

        for index, result in enumerate(
            results,
            start=1,
        ):
            metadata = result.metadata

            source = cls._source_name(result)

            page_number = int(
                metadata.get(
                    "page_number",
                    result.page_number,
                )
            )

            chunk_number = int(
                metadata.get(
                    "chunk_index",
                    0,
                )
            )

            identity = (
                source,
                page_number,
                chunk_number,
            )

            if identity in seen:
                continue

            seen.add(identity)

            sources.append(
                {
                    "reference": f"S{index}",
                    "file_name": source,
                    "page_number": page_number,
                    "chunk_number": chunk_number,
                    "score": round(
                        result.score,
                        4,
                    ),
                }
            )

        return sources

    def build_history(
        self,
        session_id: int,
        user_id: int,
        memory: ChatMemoryService,
    ) -> str:

        messages = memory.get_messages(
            session_id=session_id,
            user_id=user_id,
        )[-8:]

        return "\n".join(
            f"{message.role}: {message.message}"
            for message in messages
        )