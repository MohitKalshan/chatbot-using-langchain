"""Unit tests for input validation. No Gemini calls are made."""

import pytest

from project.schemas.movie import MovieInfo
from project.services.validation import has_title, looks_like_query


@pytest.mark.parametrize(
    "text",
    [
        "Inception is a 2010 science fiction film directed by Christopher Nolan.",
        "Finding Nemo is a 2003 animated film by Pixar.",  # starts with "Finding", not "find"
        "What Dreams May Come is a 1998 fantasy drama starring Robin Williams.",
        "The Matrix (1999) stars Keanu Reeves as Neo.",
    ],
)
def test_movie_descriptions_are_accepted(text):
    assert not looks_like_query(text)


@pytest.mark.parametrize(
    "text",
    [
        "Find movies about dreams, subconscious minds, and stealing secrets",
        "search for sci-fi films from the 90s",
        "Recommend something like Inception",
        "Show me movies with Tom Hardy",
        "  please list Christopher Nolan films  ",
    ],
)
def test_search_queries_are_rejected(text):
    assert looks_like_query(text)


@pytest.mark.parametrize(
    "text",
    [
        "What is the best movie of 2010?",
        "Who directed Inception?",
        "Can you tell me about The Matrix",
        "Is Inception worth watching ?  ",
    ],
)
def test_general_questions_are_rejected(text):
    assert looks_like_query(text)


def test_movie_with_title_is_valid():
    assert has_title(MovieInfo(title="Inception", summary="A heist inside dreams."))


@pytest.mark.parametrize("title", [None, "", "   "])
def test_movie_without_title_is_invalid(title):
    assert not has_title(MovieInfo(title=title, summary="A film about dreams."))
