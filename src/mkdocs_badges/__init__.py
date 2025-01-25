import logging

# Set up a logger for my code to use
LOGGER = logging.getLogger("mkdocs.plugins.badges")
_WARNINGS_ENABLED = True

def disable_warnings() -> None:
    global _WARNINGS_ENABLED
    _WARNINGS_ENABLED = False

def warning(message: str) -> None:
    if _WARNINGS_ENABLED:
        LOGGER.warning(f"[badges] {message}")

def warning_for_entry(badge_entry, message: str) -> None:
    if _WARNINGS_ENABLED:
        LOGGER.warning(f"[badges] [{badge_entry.file_name}:{badge_entry.line_index+1}] {message}")

def warning_for_location(file_name, line_index, message: str) -> None:
    if _WARNINGS_ENABLED:
        LOGGER.warning(f"[badges] [{file_name}:{line_index+1}] {message}")


# Import local files in the correct order
from .plugin import BadgesPlugin

__all__ = ["BadgesPlugin"]
