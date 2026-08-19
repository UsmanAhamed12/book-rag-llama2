# app/retrieval/models.py

from dataclasses import dataclass
from typing import Any


@dataclass
class RetrievalResult:
    text: str
    score: float
    metadata: dict[str, Any]
    document_id: str
    page_number: int
