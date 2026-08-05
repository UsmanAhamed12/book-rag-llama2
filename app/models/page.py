from dataclasses import dataclass

@dataclass(slots=True)
class Page:
    text: str
    page_number: int
    source: str