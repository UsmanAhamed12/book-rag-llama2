import argparse
import json
from pathlib import Path

from sentence_transformers import CrossEncoder

from app.core.container import container
from app.evaluation.dataset import load_retrieval_examples
from app.evaluation.document_scoped_retriever import DocumentScopedEvaluationRetriever
from app.evaluation.metrics import evaluate_retrieval
from app.evaluation.reranker import CrossEncoderReranker
from app.retrieval.models import RetrievalResult


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare vector retrieval against cross-encoder reranking.",
    )
    parser.add_argument(
        "--dataset",
        default="data/evaluation/retrieval_benchmark.json",
    )
    parser.add_argument(
        "--document-id",
        default="9",
    )
    parser.add_argument(
        "--candidate-k",
        type=int,
        default=20,
    )
    parser.add_argument(
        "--model",
        default="cross-encoder/ms-marco-MiniLM-L6-v2",
    )
    parser.add_argument(
        "--output",
        default="data/evaluation/retrieval_reranked.json",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.candidate_k <= 0:
        raise ValueError("candidate-k must be greater than zero")

    examples = load_retrieval_examples(args.dataset)

    # Evaluation intentionally starts from the plain vector retriever. Production
    # may already wrap it with RerankingRetriever when RERANKING_ENABLED=true,
    # but this benchmark must compare vector-only candidates against one explicit
    # reranking pass without weakening the legacy document-scoped evaluation path.
    retriever = DocumentScopedEvaluationRetriever(container.vector_retriever)

    print(f"Loading cross-encoder: {args.model}")
    model = CrossEncoder(args.model)
    reranker = CrossEncoderReranker(model)

    candidate_results: list[list[RetrievalResult]] = []
    reranked_results: list[list[RetrievalResult]] = []

    for index, example in enumerate(examples, start=1):
        candidates = retriever.search(
            query=example.question,
            user_id=0,
            document_ids=[args.document_id],
            top_k=args.candidate_k,
        )
        candidate_results.append(candidates)

        reranked = reranker.rerank(
            query=example.question,
            results=candidates,
            top_k=args.candidate_k,
        )
        reranked_results.append(
            [
                item.result
                for item in reranked
                if isinstance(item.result, RetrievalResult)
            ]
        )

        print(
            f"[{index:02d}/{len(examples)}] reranked "
            f"{len(candidates)} candidates"
        )

    report: dict[str, object] = {
        "dataset": str(args.dataset),
        "document_id": args.document_id,
        "candidate_k": args.candidate_k,
        "model": args.model,
        "examples": len(examples),
        "baseline": {},
        "reranked": {},
    }

    baseline_report: dict[str, dict[str, int | float]] = {}
    reranked_report: dict[str, dict[str, int | float]] = {}

    for k in (1, 3, 5):
        baseline = evaluate_retrieval(
            examples=examples,
            ranked_results=candidate_results,
            k=k,
        )
        reranked = evaluate_retrieval(
            examples=examples,
            ranked_results=reranked_results,
            k=k,
        )

        baseline_report[str(k)] = {
            "examples": baseline.examples,
            "hit_rate_at_k": baseline.hit_rate_at_k,
            "recall_at_k": baseline.recall_at_k,
            "mean_reciprocal_rank": baseline.mean_reciprocal_rank,
        }
        reranked_report[str(k)] = {
            "examples": reranked.examples,
            "hit_rate_at_k": reranked.hit_rate_at_k,
            "recall_at_k": reranked.recall_at_k,
            "mean_reciprocal_rank": reranked.mean_reciprocal_rank,
        }

        print(f"\nTop-K = {k}")
        print(
            "Vector   "
            f"Hit={baseline.hit_rate_at_k:.4f} "
            f"Recall={baseline.recall_at_k:.4f} "
            f"MRR={baseline.mean_reciprocal_rank:.4f}"
        )
        print(
            "Reranked "
            f"Hit={reranked.hit_rate_at_k:.4f} "
            f"Recall={reranked.recall_at_k:.4f} "
            f"MRR={reranked.mean_reciprocal_rank:.4f}"
        )

    report["baseline"] = baseline_report
    report["reranked"] = reranked_report

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print(f"\nSaved reranking benchmark to {output_path}")


if __name__ == "__main__":
    main()
