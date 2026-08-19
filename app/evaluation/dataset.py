import json
from pathlib import Path
from typing import TypedDict

from app.evaluation.models import RetrievalExample


class RawRelevantChunk(TypedDict):
    page_number: int
    chunk_index: int


class RawRetrievalExample(TypedDict):
    id: str
    question: str
    document_id: str
    relevant_chunks: list[RawRelevantChunk]


def load_retrieval_examples(path: str | Path) -> list[RetrievalExample]:
    """Load and validate a JSON retrieval benchmark dataset."""

    dataset_path = Path(path)

    if not dataset_path.exists():
        raise FileNotFoundError(f"Benchmark dataset not found: {dataset_path}")

    raw_data = json.loads(dataset_path.read_text(encoding="utf-8"))

    if not isinstance(raw_data, list):
        raise ValueError("Benchmark dataset must be a JSON array")

    examples: list[RetrievalExample] = []

    for index, raw_example in enumerate(raw_data, start=1):
        if not isinstance(raw_example, dict):
            raise ValueError(f"Benchmark item {index} must be an object")

        question = raw_example.get("question")
        document_id = raw_example.get("document_id")
        relevant_chunks = raw_example.get("relevant_chunks")

        if not isinstance(question, str) or not question.strip():
            raise ValueError(f"Benchmark item {index} has an invalid question")

        if not isinstance(document_id, str) or not document_id.strip():
            raise ValueError(f"Benchmark item {index} has an invalid document_id")

        if not isinstance(relevant_chunks, list) or not relevant_chunks:
            raise ValueError(f"Benchmark item {index} has no relevant_chunks")

        identities: set[tuple[str, int, int]] = set()

        for chunk in relevant_chunks:
            if not isinstance(chunk, dict):
                raise ValueError(
                    f"Benchmark item {index} contains an invalid relevant chunk"
                )

            page_number = chunk.get("page_number")
            chunk_index = chunk.get("chunk_index")

            if not isinstance(page_number, int) or isinstance(page_number, bool):
                raise ValueError(
                    f"Benchmark item {index} has an invalid page_number"
                )

            if not isinstance(chunk_index, int) or isinstance(chunk_index, bool):
                raise ValueError(
                    f"Benchmark item {index} has an invalid chunk_index"
                )

            identities.add((document_id, page_number, chunk_index))

        examples.append(
            RetrievalExample(
                question=question.strip(),
                relevant_chunks=frozenset(identities),
            )
        )

    if not examples:
        raise ValueError("Benchmark dataset must contain at least one example")

    return examples
