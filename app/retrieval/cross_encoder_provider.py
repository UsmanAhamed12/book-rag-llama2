from typing import Any, cast

from sentence_transformers import CrossEncoder


class CrossEncoderProvider:
    """Lazily load and reuse one cross-encoder model instance."""

    def __init__(self, model_name: str) -> None:
        self.model_name = model_name
        self._model: CrossEncoder | None = None

    @property
    def model(self) -> CrossEncoder:
        if self._model is None:
            self._model = CrossEncoder(self.model_name)
        return self._model

    def predict(self, sentences: list[tuple[str, str]]) -> list[float]:
        raw_scores = self.model.predict(cast(Any, sentences))
        return [float(score) for score in raw_scores]
