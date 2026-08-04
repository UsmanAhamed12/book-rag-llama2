# from dataclasses import dataclass
# from pathlib import Path


# @dataclass(slots=True)
# class Document:
#     """Represents a loaded document."""

#     document_id: str
#     file_name: str
#     file_path: Path
#     text: str

from dataclasses import dataclass


@dataclass(slots=True)
class Document:
    text: str
    page_number: int
    source: str