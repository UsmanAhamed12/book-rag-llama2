import ollama


class OllamaClient:
    def __init__(
        self,
        model: str = "llama3.2",
    ) -> None:
        self.model = model

    def generate(
        self,
        prompt: str,
    ) -> str:
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            return response["message"]["content"]

        except Exception:
            return (
                "I’m unable to reach the Ollama service right now, so I’m using "
                "a fallback response. Please make sure Ollama is installed and "
                "running to get the full model-generated answer."
            )

    def generate_or_none(
        self,
        prompt: str,
    ) -> str | None:
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            content = response["message"]["content"].strip()

            return content or None

        except Exception:
            return None