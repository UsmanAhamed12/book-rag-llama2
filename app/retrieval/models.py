from dataclasses import dataclass


@dataclass
class RetrievalResult:
    text: str
    score: float
    metadata: dict
    document_id: str
    page_number: int