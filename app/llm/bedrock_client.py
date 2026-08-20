from typing import Any

import boto3

from app.core.settings import settings


class BedrockClient:
    """Generate text with Amazon Bedrock's Converse API."""

    def __init__(
        self,
        model: str | None = None,
        region: str | None = None,
    ) -> None:
        self.model = model or settings.bedrock_model
        self.region = region or settings.bedrock_region
        self.client = boto3.client("bedrock-runtime", region_name=self.region)

    def generate(self, prompt: str) -> str:
        response = self._converse(prompt)
        if response is not None:
            return response

        return (
            "I’m unable to reach the language model right now. "
            "Please try again in a moment."
        )

    def generate_or_none(self, prompt: str) -> str | None:
        return self._converse(prompt)

    def _converse(self, prompt: str) -> str | None:
        try:
            response: dict[str, Any] = self.client.converse(
                modelId=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [{"text": prompt}],
                    }
                ],
                inferenceConfig={
                    "maxTokens": 1600,
                    "temperature": 0.1,
                    "topP": 0.9,
                },
            )

            output = response.get("output")
            if not isinstance(output, dict):
                return None
            message = output.get("message")
            if not isinstance(message, dict):
                return None
            content = message.get("content")
            if not isinstance(content, list) or not content:
                return None
            first_block = content[0]
            if not isinstance(first_block, dict):
                return None
            text = first_block.get("text")
            if not isinstance(text, str):
                return None

            normalized = text.strip()
            return normalized or None
        except Exception:
            return None
