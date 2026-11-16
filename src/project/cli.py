"""Shared helpers for the interactive terminal apps."""

from collections.abc import Iterator

from project.config.settings import EXIT_COMMANDS


def prompt_loop(label: str) -> Iterator[str]:
    """Yield non-empty user inputs until the user types exit/quit or presses Ctrl+C/Ctrl+D."""
    while True:
        try:
            text = input(label).strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if text.lower() in EXIT_COMMANDS:
            break
        if text:
            yield text
    print("Goodbye!")
