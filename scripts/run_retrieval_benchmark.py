import argparse
import json
from pathlib import Path

from app.core.container import container
from app.evaluation.benchmark import RetrievalBenchmark
from app.evaluation.dataset import load_retrieval_examples
from app.evaluation.diagnostics import build_retrieval_diagnostic
from app.evaluation.document_scoped_retriever import DocumentScopedEvaluationRetriever


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
    parser.add_argument(
        "--diagnostics-output",
        default="data/evaluation/retrieval_diagnostics.json",
        help="Path for the per-question diagnostic JSON report.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    examples = load_retrieval_examples(args.dataset)
    k_values = args.k_values or [1, 3, 5]

    if any(k <= 0 for k in k_values):
        raise ValueError("All k values must be greater than zero")

    evaluation_retriever = DocumentScopedEvaluationRetriever(container.retriever)

    report: dict[str, object] = {
        "dataset": str(args.dataset),
        "document_id": args.document_id,
        "scope": "document_only_legacy_evaluation",
        "examples": len(examples),
        "results": {},
    }
    results_by_k: dict[str, dict[str, int | float]] = {}

    for k in k_values:
        benchmark = RetrievalBenchmark(
            retriever=evaluation_retriever,  # type: ignore[arg-type]
            user_id=0,
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

    diagnostic_k = max(k_values)
    diagnostic_rows: list[dict[str, object]] = []

    print(f"\nPer-question diagnostics (Top-{diagnostic_k})")
    print("=" * 80)

    for index, example in enumerate(examples, start=1):
        retrieved = evaluation_retriever.search(
            query=example.question,
            user_id=0,
            document_ids=[args.document_id],
            top_k=diagnostic_k,
        )
        diagnostic = build_retrieval_diagnostic(
            example=example,
            results=retrieved,
            k=diagnostic_k,
        )

        retrieved_rows = [
            {
                "rank": item.rank,
                "document_id": item.document_id,
                "page_number": item.page_number,
                "chunk_index": item.chunk_index,
                "score": item.score,
                "is_relevant": item.is_relevant,
            }
            for item in diagnostic.retrieved
        ]
        expected_rows = [
            {
                "document_id": document_id,
                "page_number": page_number,
                "chunk_index": chunk_index,
            }
            for document_id, page_number, chunk_index in diagnostic.expected_chunks
        ]
        diagnostic_rows.append(
            {
                "question_number": index,
                "question": diagnostic.question,
                "expected_chunks": expected_rows,
                "first_relevant_rank": diagnostic.first_relevant_rank,
                "retrieved": retrieved_rows,
            }
        )

        rank_label = (
            str(diagnostic.first_relevant_rank)
            if diagnostic.first_relevant_rank is not None
            else f">{diagnostic_k}"
        )
        print(f"\n[{index:02d}] {diagnostic.question}")
        print(f"First relevant rank: {rank_label}")
        for item in diagnostic.retrieved:
            marker = "PASS" if item.is_relevant else "MISS"
            print(
                f"  #{item.rank} page={item.page_number} "
                f"chunk={item.chunk_index} score={item.score:.4f} {marker}"
            )

    diagnostics_report = {
        "dataset": str(args.dataset),
        "document_id": args.document_id,
        "top_k": diagnostic_k,
        "examples": len(examples),
        "diagnostics": diagnostic_rows,
    }
    diagnostics_path = Path(args.diagnostics_output)
    diagnostics_path.parent.mkdir(parents=True, exist_ok=True)
    diagnostics_path.write_text(
        json.dumps(diagnostics_report, indent=2),
        encoding="utf-8",
    )
    print(f"\nSaved diagnostic report to {diagnostics_path}")


if __name__ == "__main__":
    main()
