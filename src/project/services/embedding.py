"""Turn text into a vector embedding with a local Sentence Transformers model."""

from functools import cache

from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384


@cache
def _model() -> SentenceTransformer:
    """Load the model once; later calls reuse the same instance."""
    try:
        return SentenceTransformer(MODEL_NAME)
    except Exception as error:
        raise RuntimeError(f"Could not load embedding model {MODEL_NAME}: {error}") from error


def generate_embedding(text: str) -> list[float]:
    """Return a 384-number embedding for the given text."""
    if not text or not text.strip():
        raise ValueError("Cannot embed empty text")

    try:
        vector = _model().encode(text)
    except RuntimeError:
        raise
    except Exception as error:
        raise RuntimeError(f"Could not create embedding: {error}") from error

    return [float(value) for value in vector]
