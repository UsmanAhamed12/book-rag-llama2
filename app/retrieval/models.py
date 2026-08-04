from dataclasses import dataclass


@dataclass(slots=True)
class RetrievalResult:
    text: str
    score: float
    metadata: dict