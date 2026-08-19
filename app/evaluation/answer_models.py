from dataclasses import dataclass


@dataclass(frozen=True)
class AnswerEvaluationExample:
    """Expected behavior for one grounded-answer evaluation example."""

    question: str
    answerable: bool
    available_sources: frozenset[str]


@dataclass(frozen=True)
class AnswerEvaluationResult:
    """Deterministic checks for one generated answer."""

    citation_present: bool
    citations_valid: bool
    refusal_correct: bool
    leaked_internal_markup: bool

    @property
    def passed(self) -> bool:
        return (
            self.citation_present
            and self.citations_valid
            and self.refusal_correct
            and not self.leaked_internal_markup
        )


@dataclass(frozen=True)
class AnswerEvaluationSummary:
    """Aggregate deterministic grounded-answer metrics."""

    examples: int
    pass_rate: float
    citation_presence_rate: float
    citation_validity_rate: float
    refusal_accuracy: float
    internal_markup_leak_rate: float
