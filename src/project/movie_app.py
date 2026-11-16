"""Interactive app: paragraph -> structured info + summary -> JSON -> SQLite."""

from project.cli import prompt_loop
from project.config.settings import DB_PATH
from project.database.db import connect, save_movie
from project.services.movie_extractor import extract_movie_info


def run() -> None:
    print("\nMovie Info Extractor")
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
            movie_id = save_movie(conn, movie, paragraph)
            print(f"Saved with id {movie_id}")


if __name__ == "__main__":
    run()
