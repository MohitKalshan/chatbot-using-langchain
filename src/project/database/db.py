"""SQLite storage for extracted movies."""

import json
import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

from project.config.settings import DB_PATH
from project.schemas.movie import MovieInfo

SCHEMA = """
CREATE TABLE IF NOT EXISTS movies (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    title        TEXT,
    release_year INTEGER,
    director     TEXT,
    genres       TEXT NOT NULL,  -- JSON list
    "cast"       TEXT NOT NULL,  -- JSON list
    rating       REAL,
    box_office   TEXT,
    summary      TEXT NOT NULL,
    raw_text     TEXT NOT NULL,
    created_at   TEXT DEFAULT CURRENT_TIMESTAMP
)
"""


@contextmanager
def connect(db_path: Path = DB_PATH) -> Iterator[sqlite3.Connection]:
    """Open the database, make sure the table exists, and always close the connection."""
    conn = sqlite3.connect(db_path)
    try:
        conn.execute(SCHEMA)
        yield conn
    finally:
        conn.close()


def get_summaries(conn: sqlite3.Connection) -> list[tuple[int, str | None, str]]:
    """Return (id, title, summary) for every saved movie."""
    return conn.execute("SELECT id, title, summary FROM movies ORDER BY id").fetchall()


def normalize_title(title: str) -> str:
    """'  The  Matrix ' -> 'the matrix'"""
    return " ".join(title.lower().split())


def find_duplicate(conn: sqlite3.Connection, movie: MovieInfo) -> int | None:
    """Return the id of an existing movie with the same title and year, or None."""
    if not movie.title:
        return None  # nothing to match on
    row = conn.execute(
        "SELECT id FROM movies WHERE lower(trim(title)) = ? AND release_year IS ?",
        (normalize_title(movie.title), movie.release_year),
    ).fetchone()
    return row[0] if row else None


def save_movie(conn: sqlite3.Connection, movie: MovieInfo, raw_text: str) -> int:
    """Insert a movie and return its new row id."""
    with conn:  # commits on success, rolls back on error
        cursor = conn.execute(
            """
            INSERT INTO movies
                (title, release_year, director, genres, "cast", rating, box_office, summary, raw_text)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                movie.title,
                movie.release_year,
                movie.director,
                json.dumps(movie.genres),
                json.dumps(movie.cast),
                movie.rating,
                movie.box_office,
                movie.summary,
                raw_text,
            ),
        )
    return cursor.lastrowid
