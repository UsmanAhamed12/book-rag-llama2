from collections.abc import Sequence

from app.retrieval.models import RetrievalResult
from app.retrieval.retriever import Retriever


class DocumentScopedEvaluationRetriever:
    """Evaluate legacy indexed chunks without weakening production user filtering.

    This adapter deliberately requires one or more document IDs and queries only
    those documents. The ``user_id`` argument is accepted for compatibility with
    ``RetrievalBenchmark