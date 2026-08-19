import json

from app.llm.service import LLMService
from app.retrieval.retriever import Retriever


class DocumentProfileService:
    def __init__(
        self,
        retriever: Retriever,
        llm: LLMService,
    ) -> None:
        self.retriever = retriever
        self.llm = llm

    def build_profile(
        self,
        user_id: int,
        document_id: str,
        filename: str,
    ) -> tuple[str, list[str]]:
        chunks = self.retriever.get_representative_chunks(
            user_id=user_id,
            document_id=document_id,
            sample_count=10,
        )

        if not chunks:
            return (
                "No usable text was found for this document.",
                [],
            )

        context = "\n\n".join(
            (f"Page {result.page_number}:\n{result.text}") for result in chunks
        )

        prompt = f"""
You are creating a compact profile for one uploaded document.

Document filename:
{filename}

Representative document excerpts:

{context}

Return valid JSON only using exactly this structure:

{{
  "summary": "A concise 2-4 paragraph summary of the document.",
  "topics": [
    "topic 1",
    "topic 2"
  ]
}}

Rules:
- Use only the supplied excerpts.
- Do not invent chapters, authors, publishers, or topics.
- Describe the document conservatively if the excerpts are incomplete.
- Include at most 8 major topics.
- Do not include markdown.
"""

        response = self.llm.answer(
            prompt,
        )

        try:
            data = json.loads(response)

            summary = str(
                data.get(
                    "summary",
                    "",
                )
            ).strip()

            raw_topics = data.get(
                "topics",
                [],
            )

            topics = [str(topic).strip() for topic in raw_topics if str(topic).strip()][
                :8
            ]

            if not summary:
                raise ValueError(
                    "Document summary was empty.",
                )

            return summary, topics

        except (
            json.JSONDecodeError,
            TypeError,
            ValueError,
        ):
            return (
                response.strip(),
                [],
            )
