import urllib
# local files
from . import LOGGER
from .parser import ParsedBadge, BadgeException, parse_file
from .badge_html import generate_badge_html
from .install_badge import InstallBadgeManager

LINK_BADGE_EMPTY_FIELDS = ["copy_text", "link", "reflink"]
REFLINK_BADGE_EMPTY_FIELDS = LINK_BADGE_EMPTY_FIELDS
INSTALL_BADGE_EMPTY_FIELDS = LINK_BADGE_EMPTY_FIELDS
COPY_BADGE_EMPTY_FIELDS = LINK_BADGE_EMPTY_FIELDS
STRIP_SUBDOMAINS = [
    "www", # Pretty standard prefix for websites
    "m", # Pretty standard for mobile sites
]

def replace_badges(markdown: str, install_badge_manager: InstallBadgeManager) -> str:
    lines = markdown.split("\n")
    for parser_result_entry in parse_file(lines):
        try:
            index = parser_result_entry.line_index
            badge = parser_result_entry.parsed_badge

            lines[index] = format_badge(badge, install_badge_manager)
        except BadgeException as error:
            LOGGER.warning(f"Badge processing error: {error}")
    
    return "\n".join(lines)


def format_badge(badge: ParsedBadge, install_badge_manager: InstallBadgeManager) -> str:
    badge.check_fields()
    typ = badge.badge_type
    if not typ:
        # TODO: Make it possible to use copy_text and reflink at the same time
        if badge.reflink:
            badge.assert_empty("copy_text")

        classes = ["badge-normal", *badge.html_classes]
        if badge.reflink:
            classes.append("badge-reflink")
        badge_html = generate_badge_html(badge.title, badge.value, copy_text=badge.copy_text, link=badge.link, extra_classes=classes)
        if badge.reflink:
            badge_html = f"[{badge_html}][{badge.reflink}]"
        return badge_html
    
    elif typ == "L":
        badge.assert_all_empty(LINK_BADGE_EMPTY_FIELDS)
        simplified_host_name = get_simplified_hostname(badge.value)
        classes = ["badge-link", *badge.html_classes]
        return generate_badge_html(badge.title, simplified_host_name, link=badge.value, extra_classes=classes)

    elif typ == "R":
        badge.assert_all_empty(REFLINK_BADGE_EMPTY_FIELDS)
        classes = ["badge-reflink", *badge.html_classes]
        badge_html = generate_badge_html(badge.title, badge.value, extra_classes=classes)
        return f"[{badge_html}][{badge.value}]"

    elif typ == "I":
        return install_badge_manager.format_badge(badge)
    
    elif typ == "C":
        badge.assert_all_empty(COPY_BADGE_EMPTY_FIELDS)
        classes = ["badge-copy", *badge.html_classes]
        return generate_badge_html(badge.title, badge.value, copy_text=badge.value, extra_classes=classes)

    else:
        raise BadgeException(f"Unknown badge type '{typ}'")


def get_simplified_hostname(url: str) -> str:
    url = url.strip()
    simplified_host_name = urllib.parse.urlparse(url).netloc
    if not simplified_host_name:
        raise Exception(f"No hostname in URL: '{url}'")
    
    # Remove unnecessary subdomains: for example "www.example.com" -> "example.com"
    parts = simplified_host_name.split(".")
    if len(parts) >= 2: # only handle www.example.com, but not www.com
        if parts[0] in STRIP_SUBDOMAINS:
            # remove the first subdomain
            parts = parts[1:]
            # store our change in the original variable
            simplified_host_name = ".".join(parts)
    
    return simplified_host_name

