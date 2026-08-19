import argparse
import json
from pathlib import Path

from app.core.container import container
from app.evaluation.benchmark import RetrievalBenchmark
from app.evaluation.dataset import load_retrieval_examples


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the labeled retrieval benchmark against ChromaDB.",
    )
    parser.add_argument(
        "--dataset",
        default="data/evaluation/retrieval_benchmark.json",
        help="Path to the labeled benchmark JSON file.",
    )
    parser.add_argument(
        "--document-id",
        default="9",
        help="Restrict retrieval to this indexed document ID.",
    )
    parser.add_argument(
        "--user-id",
        type=int,
        required=True,
        help="Owner user ID stored in Chroma metadata.",
    )
    parser.add_argument(
        "--k",
        type=int,
        action="append",
        dest="k_values",
        help="Top-K value to evaluate. Repeat for multiple values.",
    )
    parser.add_argument(
        "--output",
        default="data/evaluation/retrieval_baseline.json",
        help="Path for the JSON benchmark report.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    examples = load_retrieval_examples(args.dataset)
    k_values = args.k_values or [1, 3, 5]

    if any(k <= 0 for k in k_values):
        raise ValueError("All k values must be greater than zero")

    report: dict[str, object] = {
        "dataset": str(args.dataset),
        "document_id": args.document_id,
        "user_id": args.user_id,
        "examples": len(examples),
        "results": {},
    }
    results_by_k: dict[str, dict[str, int | float]] = {}

    for k in k_values:
        benchmark = RetrievalBenchmark(
            retriever=container.retriever,
            user_id=args.user_id,
            top_k=k,
        )
        evaluation = benchmark.run(
            examples,
            document_ids=[args.document_id],
        )
        result = benchmark.to_report(evaluation)
        results_by_k[str(k)] = result

        print(f"\nTop-K = {k}")
        print(f"Examples:   {evaluation.examples}")
        print(f"Hit Rate:   {evaluation.hit_rate_at_k:.4f}")
        print(f"Recall:     {evaluation.recall_at_k:.4f}")
        print(f"MRR:        {evaluation.mean_reciprocal_rank:.4f}")

    report["results"] = results_by_k

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    print(f"\nSaved benchmark report to {output_path}")


if __name__ == "__main__":
    main()
