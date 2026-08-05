from dataclasses import dataclass
from pathlib import Path

@dataclass(slots=True)
class Document:
    document_id: str
    file_name: str
    file_path: Path