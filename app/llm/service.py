from app.llm.ollama_client import OllamaClient


class LLMService:
    def __init__(self) -> None:

        self.client = OllamaClient()

    def answer(
        self,
        prompt: str,
    ) -> str:

        return self.client.generate(prompt)
