"""Decide whether input is a movie description worth extracting and saving."""

from project.schemas.movie import MovieInfo

INVALID_INPUT_MESSAGE = "This does not appear to be a movie description. Please enter a movie paragraph."

# Inputs starting with these words are requests, not descriptions.
# Whole words only, so "Finding Nemo is a 2003 film..." is still accepted.
REQUEST_STARTS = (
    "find", "search", "recommend", "suggest", "list",
    "show me", "give me", "tell me", "can you", "could you", "please",
)


def looks_like_query(text: str) -> bool:
    """True for search queries and questions, e.g. 'Find movies about dreams'."""
    text = text.strip().lower()
    if text.endswith("?"):
        return True
    words = text.split()
    return any(words[: len(start.split())] == start.split() for start in REQUEST_STARTS)


def has_title(movie: MovieInfo) -> bool:
    """A record without a title can't be identified, so it isn't saved."""
    return bool(movie.title and movie.title.strip())
