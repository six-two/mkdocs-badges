import re
# local files
from . import replace_regex_matches
from .badge_html import generate_badge_html


# |"badge name":value|
REGEX = re.compile('\|"([^"]+)":([^\|]+)\|')


def replace_function(match: re.Match) -> str:
    badge_type = match.group(1)
    badge_value = match.group(2)
    return generate_badge_html(badge_type, badge_value)


def replace_normal_badges(text: str) -> str:
    return replace_regex_matches(REGEX, text, replace_function)

