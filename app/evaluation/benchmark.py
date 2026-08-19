from collections.abc import Sequence
from dataclasses import asdict

from app.evaluation.metrics import evaluate_retrieval
from app.evaluation.models import RetrievalEvaluation, RetrievalExample
from app.retrieval.models import RetrievalResult
from app.retrieval.retriever import Retriever


class RetrievalBenchmark:
    """Run deterministic labeled retrieval benchmarks against the live retriever."""

    def __init__(
        self,
        retriever: Retriever,
        user_id: int,
        top_k: int = 5,
    ) -> None:
        if top_k <= 0:
            raise ValueError("top_k must be greater than zero")

        self.retriever = retriever
        self.user_id = user_id
        self.top_k = top_k

    def run(
        self,
        examples: Sequence[RetrievalExample],
        document_ids: list[str] | None = None,
    ) -> RetrievalEvaluation:
        ranked_results: list[list[RetrievalResult]] = []

        for example in examples:
            ranked_results.append(
                self.retriever.search(
                    query=example.question,
                    user_id=self.user_id,
                    document_ids=document_ids,
                    top_k=self.top_k,
                )
            )

        return evaluate_retrieval(
            examples=examples,
            ranked_results=ranked_results,
            k=self.top_k,
        )

    @staticmethod
    def to_report(evaluation: RetrievalEvaluation) -> dict[str, int | float]:
        return asdict(evaluation)
