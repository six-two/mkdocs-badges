from typing import Callable
from re import Pattern, Match


def replace_regex_matches(compiled_regex: Pattern, text: str, replace_function: Callable[[Match], str]) -> str:
    """
    Replace all non-overlapping occurences of the given regex
    A badge will only be recodnized, if it is the only thing in its line.
    It will not be detected, if it is a code block (indented or in ``` block)
    """
    # Process the text line by line
    lines = text.split("\n")
    is_in_code_block = False
    for index, line in enumerate(lines):
        # the badge needs to start at the beginning of the line
        if line.strip().startswith("```"):
            is_in_code_block = not is_in_code_block
        elif not is_in_code_block:
            # check if the line is a bagde
            line = line.rstrip() # ignore any whitespace after the badge
            # print(index, repr(line))
            # Only accept full matches
            match = compiled_regex.fullmatch(line)

            if match:
                # derive the replacement thext from the match object
                replacement = str(replace_function(match))

                # Replace the badge line with the replacement
                lines[index] = replacement
        else:
            # We are inside a code block -> don't try to interpret badges
            pass
    
    # Convert the lines back to a single string
    return "\n".join(lines)
