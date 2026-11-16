"""Generate embeddings for every saved movie summary (read-only: the database is not changed)."""

import sys

sys.path.insert(0, "src")

from project.database.db import connect, get_summaries
from project.services.embedding import generate_embedding


def main() -> None:
    with connect() as conn:
        movies = get_summaries(conn)

    if not movies:
        print("No movies saved yet. Run main.py first.")
        return

    for movie_id, title, summary in movies:
        embedding = generate_embedding(summary)
        print(f"{movie_id}: {title or '(no title)'} -> {len(embedding)} dimensions")


if __name__ == "__main__":
    main()
