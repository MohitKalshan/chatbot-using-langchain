"""Project-wide settings, loaded once from the environment (.env)."""

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DB_PATH = Path(os.getenv("MOVIES_DB_PATH", PROJECT_ROOT / "movies.db"))

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
EXIT_COMMANDS = {"exit", "quit"}


def require_env(name: str) -> str:
    """Return an environment variable or exit with a clear message if it is missing."""
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"{name} not found. Add it to your .env file.")
    return value
