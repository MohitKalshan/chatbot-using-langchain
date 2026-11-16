"""Unit tests for the embedding service. The real model is mocked, so nothing is downloaded."""

from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from project.services import embedding
from project.services.embedding import EMBEDDING_DIM, generate_embedding


@pytest.fixture
def fake_model():
    """Replace SentenceTransformer with a fake that returns a 384-number vector."""
    embedding._model.cache_clear()
    model = MagicMock()
    model.encode.return_value = np.full(EMBEDDING_DIM, 0.5, dtype=np.float32)
    with patch.object(embedding, "SentenceTransformer", return_value=model) as loader:
        yield loader, model
    embedding._model.cache_clear()


def test_valid_summary_returns_384_floats(fake_model):
    result = generate_embedding("A thief enters dreams to steal secrets.")

    assert len(result) == EMBEDDING_DIM == 384
    assert all(isinstance(value, float) for value in result)


@pytest.mark.parametrize("text", ["", "   ", "\n\t "])
def test_empty_or_whitespace_text_is_rejected(fake_model, text):
    with pytest.raises(ValueError):
        generate_embedding(text)


def test_model_is_loaded_only_once(fake_model):
    loader, _ = fake_model

    generate_embedding("first")
    generate_embedding("second")

    assert loader.call_count == 1


def test_model_load_failure_raises_runtime_error():
    embedding._model.cache_clear()
    with patch.object(embedding, "SentenceTransformer", side_effect=OSError("no network")):
        with pytest.raises(RuntimeError, match="Could not load embedding model"):
            generate_embedding("text")
    embedding._model.cache_clear()


def test_encoding_failure_raises_runtime_error(fake_model):
    _, model = fake_model
    model.encode.side_effect = ValueError("bad input")

    with pytest.raises(RuntimeError, match="Could not create embedding"):
        generate_embedding("text")
