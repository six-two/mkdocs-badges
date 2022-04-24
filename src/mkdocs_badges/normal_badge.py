import re
# local files
from . import replace_regex_matches


# |"badge name":value|
REGEX = re.compile('\|"([^"]+)":([^\|]+)\|')


def replace_function(match: re.Match) -> str:
    badge_type = match.group(1)
    badge_value = match.group(2)
    return normal_badge(badge_type, badge_value)


def normal_badge(badge_type: str, badge_value: str) -> str:
    return ("<span class='badge'>"+
        f"<span class=title>{badge_type}</span>"+
        f"<span class=value>{badge_value}</span>"+
    "</span>")


def replace_normal_badges(text: str) -> str:
    return replace_regex_matches(REGEX, text, replace_function)

