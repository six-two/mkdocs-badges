import re
import urllib
# local files
from . import replace_regex_matches
from .badge_html import generate_badge_html


# |&badge name:link url|
# Example: |&Homepage: https://www.example.com/some/path?with=parameters#and-hash |
# Optional whitespace can be around the link to make the code easier to read
# The shown text would be the same as |"Homepage":example.com|, but with a link to the given exact URL
REGEX = re.compile('\|&([^:]+):([^\|]+)\|')
STRIP_SUBDOMAINS = [
    "www", # Pretty standard prefix for websites
    "m", # Pretty standard for mobile sites
]


def replace_function(match: re.Match) -> str:
    badge_type = match.group(1)
    badge_value = match.group(2)
    return link_badge(badge_type, badge_value)


def link_badge(badge_type: str, badge_value: str) -> str:
    # Extract the hostname
    badge_value = badge_value.strip()
    simplified_host_name = urllib.parse.urlparse(badge_value).netloc
    if not simplified_host_name:
        raise Exception(f"No hostname in URL: '{badge_value}'")
    
    # Remove unnecessary subdomains: for example "www.example.com" -> "example.com"
    parts = simplified_host_name.split(".")
    if len(parts) >= 2: # only handle www.example.com, but not www.com
        if parts[0] in STRIP_SUBDOMAINS:
            # remove the first subdomain
            parts = parts[1:]
            # store our change in the original variable
            simplified_host_name = ".".join(parts)

    return generate_badge_html(badge_type, simplified_host_name, link=badge_value)


def replace_link_badges(text: str) -> str:
    return replace_regex_matches(REGEX, text, replace_function)

