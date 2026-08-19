from typing import Any, cast

import ollama

from app.core.settings import settings


class OllamaClient:
    def __init__(
        self,
        model: str | None = None,
        host: str | None = None,
    ) -> None:
        self.model = model or settings.ollama_model
        self.host = host or settings.ollama_host

        self.client = ollama.Client(
            host=self.host,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:
        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            content = cast(
                str,
                response["message"]["content"],
            )

            return content

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
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            raw_content: Any = response["message"]["content"]

            if not isinstance(raw_content, str):
                return None

            content = raw_content.strip()

            return content or None

        except Exception:
            return None