"""Structured movie data extracted from free text."""

from pydantic import BaseModel, Field


class MovieInfo(BaseModel):
    title: str | None = Field(default=None, description="The movie's title, or null if not named")
    release_year: int | None = Field(default=None, description="Year of release, if stated")
    director: str | None = Field(default=None, description="Director's name, if stated")
    genres: list[str] = Field(default_factory=list, description="Genres, e.g. 'sci-fi', 'drama'")
    cast: list[str] = Field(default_factory=list, description="Main actors mentioned")
    rating: float | None = Field(default=None, description="Rating if mentioned, e.g. 8.8")
    box_office: str | None = Field(default=None, description="Box office earnings if mentioned, e.g. '$830 million'")
    summary: str = Field(description="A clean, neutral 2-3 sentence summary of the movie")
