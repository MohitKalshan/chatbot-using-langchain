"""Movie Information Extractor: paragraph -> structured info + summary -> JSON -> SQLite."""

import sys

sys.path.insert(0, "src")

from project.cli import prompt_loop
from project.config.settings import DB_PATH
from project.database.db import connect, find_duplicate, save_movie
from project.services.movie_extractor import extract_movie_info


def main() -> None:
    print("\nMovie Information Extractor")
    print(f"Results are saved to {DB_PATH}")
    print("Type 'exit' or 'quit' to end.")

    with connect() as conn:
        for paragraph in prompt_loop("\nPaste a movie paragraph: "):
            try:
                movie = extract_movie_info(paragraph)
            except Exception as error:
                print(f"Error: {error}")
                continue

            print(movie.model_dump_json(indent=2))

            existing_id = find_duplicate(conn, movie)
            if existing_id:
                print(f"Already saved with id {existing_id}, skipping duplicate")
                continue

            movie_id = save_movie(conn, movie, paragraph)
            print(f"Saved with id {movie_id}")


if __name__ == "__main__":
    main()
