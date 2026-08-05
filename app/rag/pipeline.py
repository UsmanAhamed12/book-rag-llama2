from app.retrieval.retriever import Retriever
from app.rag.prompt import SYSTEM_PROMPT
from app.llm.service import LLMService


class RAGPipeline:

    def __init__(
        self,
        retriever: Retriever,
        llm: LLMService
    ) -> None:

        self.retriever = retriever
        self.llm = llm


    def build_prompt(
    self,
    question: str,
    top_k: int = 5,
    ) -> str:

        results = self.retriever.search(
            question,
            top_k,
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


            context_parts.append(

                f"""
    SOURCE:
    {source}

    CHUNK:
    {chunk}

    CONTENT:
    {result.text}

    """

            )


        context = "\n\n".join(
            context_parts
        )


        return SYSTEM_PROMPT.format(
            context=context,
            question=question,
        )

    def ask(
    self,
    question: str,
):

        prompt = self.build_prompt(
            question
        )

        answer = self.llm.answer(
            prompt
        )

        return answer