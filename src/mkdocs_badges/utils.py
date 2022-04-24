from typing import Callable
from re import Pattern, Match


def replace_regex_matches(compiled_regex: Pattern, text: str, replace_function: Callable[[Match], str]) -> str:
    """
    Replace all non-overlapping occurences of the given regex
    """
    search_start_pos = 0
    while True:
        match = compiled_regex.search(text, search_start_pos)
        # Return after all matches have been replaced
        if not match:
            return text

        # derive the replacement thext from the match object
        replacement = str(replace_function(match))

        # Replace the matched text with the replacement
        start, end = match.span()
        text = text[:start] + replacement + text[end:]

        # Update the search start to be after the replacement
        search_start_pos = start + len(replacement)
