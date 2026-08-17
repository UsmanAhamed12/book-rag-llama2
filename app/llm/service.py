from app.llm.ollama_client import OllamaClient
from app.rag.document_summary_prompt import DOCUMENT_SUMMARY_PROMPT
from app.rag.query_rewriter import QUERY_REWRITE_PROMPT


class LLMService:
    def __init__(self) -> None:
        self.client = OllamaClient()

    def answer(
        self,
        prompt: str,
    ) -> str:
        return self.client.generate(prompt)

    def rewrite_query(
        self,
        question: str,
        history: str,
    ) -> str:
        if not history.strip():
            return question.strip()

        prompt = QUERY_REWRITE_PROMPT.format(
            history=history,
            question=question,
        )

        rewritten = self.client.generate_or_none(
            prompt,
        )

        return rewritten or question.strip()

    def summarize_document_profiles(
        self,
        question: str,
        profiles: str,
    ) -> str:
        prompt = DOCUMENT_SUMMARY_PROMPT.format(
            profiles=profiles,
            question=question,
        )

        return self.client.generate(prompt)