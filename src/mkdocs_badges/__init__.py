import logging

# Set up a logger for my code to use
LOGGER = logging.getLogger("mkdocs.plugins.badges")

def warning(message: str) -> None:
    LOGGER.warning(f"[badges] {message}")

# Import local files in the correct order
# from .utils import replace_regex_matches
# from .normal_badge import replace_normal_badges
from .plugin import BadgesPlugin

__all__ = ["BadgesPlugin"]
