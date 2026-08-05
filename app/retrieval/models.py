from dataclasses import dataclass


@dataclass
class RetrievalResult:

    text: str

    score: float

    metadata: dict