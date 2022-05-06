import html
import re
# local files
from . import replace_regex_matches
from .badge_html import generate_badge_html

# Title and value are required, text to copy and link are optional
# When only one of the optional ones is required, clicks on the whole badge should lead to the associated action
# |t:badge title|(c:text to copy|)?v:badge value|(l:link|)?
def part(name: str, optional: bool = False) -> str:
    regex = "\|" + name + ":([^|]+)"
    if optional:
        regex = f"(?:{regex})?"
    return regex

# Allow the |end syntax for now, it made sense in v1.1.0
REGEX = re.compile(part("t") + part("c", True) + part("v") + part("l", True) + "\|(?:end)?")


def replace_function(match: re.Match) -> str:
    group_index = 1
    badge_type, text_to_copy, badge_value, link = match.groups()
    return generate_badge_html(badge_type, badge_value, copy_text=text_to_copy or "", link=link or "")


def replace_custom_badges(text: str) -> str:
    return replace_regex_matches(REGEX, text, replace_function)

