from app.retrieval.retriever import Retriever
from app.rag.prompt import SYSTEM_PROMPT
from app.llm.service import LLMService
from app.services.chat_memory_service import ChatMemoryService


class RAGPipeline:

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
    ) -> str:

        results = self.retriever.search(
            question,
            top_k,
        )

        history = self.build_history(
    session_id
)


        context_parts = []


        for result in results:

            source = result.metadata.get(
                "document_id",
                "unknown"
            )

            chunk = result.metadata.get(
                "chunk_index",
                "unknown"
            )

            page = result.metadata.get(
                "page_number",
                "unknown"
            )


            context_parts.append(
                                f"""
                            ==========================================
                            Document: {source}
                            Page: {page}
                            Chunk: {chunk}

                            Content:
                            {result.text}
                            ==========================================
                            """
                )


        context = "\n\n".join(
            context_parts
        )


        return SYSTEM_PROMPT.format(
            history=history,
            context=context,
            question=question,
        )

    def ask(
        self,
        session_id: int,
        question: str,
    ) -> dict:

        # Save user message
        self.memory.save_message(
            session_id=session_id,
            role="user",
            message=question,
        )

        # Build prompt with conversation history + RAG context
        prompt = self.build_prompt(
            session_id=session_id,
            question=question,
        )

        # Generate answer
        answer = self.llm.answer(
            prompt
        )

        # Save assistant response
        self.memory.save_message(
            session_id=session_id,
            role="assistant",
            message=answer,
        )

        return {
            "answer": answer,
        }
    
    def build_history(
        self,
        session_id: int,
    ) -> str:

        messages = self.memory.get_messages(
            session_id
        )

        history = []

        for message in messages:

            history.append(
                f"{message.role}: {message.message}"
            )

        return "\n".join(history)