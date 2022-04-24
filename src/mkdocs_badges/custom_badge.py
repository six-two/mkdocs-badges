import html
import re
# local files
from . import replace_regex_matches
from .normal_badge import normal_badge

# Title and value are required, text to copy and link are optional
# When only one of the optional ones is required, clicks on the whole badge should lead to the associated action
# |t:badge title|(c:text to copy|)?v:badge value|(l:link|)?
def part(name: str, optional: bool = False) -> str:
    regex = "\|" + name + ":([^|]+)"
    if optional:
        regex = f"(?:{regex})?"
    return regex

REGEX = re.compile(part("t") + part("c", True) + part("v") + part("l", True) + "\|end")


def replace_function(match: re.Match) -> str:
    group_index = 1
    badge_type, text_to_copy, badge_value, link = match.groups()
    return custom_badge(badge_type, badge_value, text_to_copy or "", link or "")


def custom_badge(badge_type: str, badge_value: str, text_to_copy: str, link: str) -> str:
    on_click = f"onclick=\"on_click_badge_name('{html.escape(text_to_copy)}')\""
    href = f"href=\"{html.escape(link)}\""

    if text_to_copy and link:
        return "<span class=badge>"\
            f"<span class='title badge-copy' {on_click}>{badge_type}</span>"\
            f"<a {href}><span class=value>{badge_value}</span></a>"\
        "</span>"
    elif text_to_copy and not link:
        return f"<span class='badge badge-copy' {on_click}>"\
            f"<span class=title>{badge_type}</span>"\
            f"<span class=value>{badge_value}</span>"\
        "</span>"
    elif not text_to_copy and link:
        return f"<a class=badge {href}>"\
            f"<span class=title>{badge_type}</span>"\
            f"<span class=value>{badge_value}</span>"\
        "</a>"
    else:
        return normal_badge(badge_type, badge_value);

def replace_custom_badges(text: str) -> str:
    return replace_regex_matches(REGEX, text, replace_function)

