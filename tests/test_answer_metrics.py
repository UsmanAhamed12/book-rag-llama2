import pytest

from app.evaluation.answer_metrics import (
    evaluate_answer,
    extract_citations,
    summarize_answer_evaluations,
)
from app.evaluation.answer_models import AnswerEvaluationExample


def make_example(*, answerable: bool) -> AnswerEvaluationExample:
    return AnswerEvaluationExample(
        question="What is regression?",
        answerable=answerable,
        available_sources=frozenset({"S1", "S2"}),
    )


def test_extract_citations_returns_unique_source_labels() -> None:
    assert extract_citations("Regression is supervised learning [S1]. [S2] [S1]") == (
        frozenset({"S1", "S2"})
    )


def test_answerable_response_passes_with_valid_citation() -> None:
    result = evaluate_answer(
        make_example(answerable=True),
        "## Answer\nRegression is a supervised learning technique [S1].",
    )

    assert result.passed is True
    assert result.citation_present is True
    assert result.citations_valid is True
    assert result.refusal_correct is True
    assert result.leaked_internal_markup is False


def test_answerable_response_fails_without_citation() -> None:
    result = evaluate_answer(
        make_example(answerable=True),
        "## Answer\nRegression is a supervised learning technique.",
    )

    assert result.passed is False
    assert result.citation_present is False


def test_answer_fails_when_it_invents_source_label() -> None:
    result = evaluate_answer(
        make_example(answerable=True),
        "## Answer\nRegression is supervised learning [S9].",
    )

    assert result.passed is False
    assert result.citations_valid is False


def test_unanswerable_response_passes_with_required_refusal() -> None:
    result = evaluate_answer(
        make_example(answerable=False),
        "I cannot find this information in the provided book context.",
    )

    assert result.passed is True
    assert result.citation_present is True
    assert result.refusal_correct is True


def test_unanswerable_response_fails_if_it_answers_instead() -> None:
    result = evaluate_answer(
        make_example(answerable=False),
        "## Answer\nThe answer is definitely 42 [S1].",
    )

    assert result.passed is False
    assert result.refusal_correct is False
    assert result.citation_present is False


def test_internal_prompt_markup_is_detected() -> None:
    result = evaluate_answer(
        make_example(answerable=True),
        "Retrieved Context:\n<document_text>Regression</document_text> [S1]",
    )

    assert result.passed is False
    assert result.leaked_internal_markup is True


def test_summary_aggregates_answer_metrics() -> None:
    results = [
        evaluate_answer(
            make_example(answerable=True),
            "Regression is supervised learning [S1].",
        ),
        evaluate_answer(
            make_example(answerable=False),
            "I cannot find this information in the provided book context.",
        ),
    ]

    summary = summarize_answer_evaluations(results)

    assert summary.examples == 2
    assert summary.pass_rate == 1.0
    assert summary.citation_presence_rate == 1.0
    assert summary.citation_validity_rate == 1.0
    assert summary.refusal_accuracy == 1.0
    assert summary.internal_markup_leak_rate == 0.0


def test_summary_rejects_empty_results() -> None:
    with pytest.raises(ValueError, match="at least one"):
        summarize_answer_evaluations([])
