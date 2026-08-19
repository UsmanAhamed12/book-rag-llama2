import re

from app.evaluation.answer_models import (
    AnswerEvaluationExample,
    AnswerEvaluationResult,
    AnswerEvaluationSummary,
)

_REFUSAL = "I cannot find this information in the provided book context."
_CITATION_PATTERN = re.compile(r"\[(S\d+)\]")
_INTERNAL_MARKERS = (
    "<document_text>",
    "</document_text>",
    "Retrieved Context:",
    "Grounding Rules",
    "Citation Rules",
    "system instructions",
    "prompt instructions",
)


def extract_citations(answer: str) -> frozenset[str]:
    """Extract unique source labels such as S1 and S2 from an answer."""

    return frozenset(_CITATION_PATTERN.findall(answer))


def evaluate_answer(
    example: AnswerEvaluationExample,
    answer: str,
) -> AnswerEvaluationResult:
    """Evaluate deterministic citation, refusal, and leakage requirements."""

    citations = extract_citations(answer)
    is_refusal = _REFUSAL in answer

    citation_present = bool(citations) if example.answerable else not citations
    citations_valid = citations.issubset(example.available_sources)
    refusal_correct = (not is_refusal) if example.answerable else is_refusal
    leaked_internal_markup = any(marker in answer for marker in _INTERNAL_MARKERS)

    return AnswerEvaluationResult(
        citation_present=citation_present,
        citations_valid=citations_valid,
        refusal_correct=refusal_correct,
        leaked_internal_markup=leaked_internal_markup,
    )


def summarize_answer_evaluations(
    results: list[AnswerEvaluationResult],
) -> AnswerEvaluationSummary:
    """Aggregate deterministic grounded-answer metrics."""

    if not results:
        raise ValueError("results must contain at least one evaluation")

    count = len(results)

    return AnswerEvaluationSummary(
        examples=count,
        pass_rate=sum(result.passed for result in results) / count,
        citation_presence_rate=(
            sum(result.citation_present for result in results) / count
        ),
        citation_validity_rate=(
            sum(result.citations_valid for result in results) / count
        ),
        refusal_accuracy=sum(result.refusal_correct for result in results) / count,
        internal_markup_leak_rate=(
            sum(result.leaked_internal_markup for result in results) / count
        ),
    )
