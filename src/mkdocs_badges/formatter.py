from urllib.parse import urlparse

# local files
from . import LOGGER
from .parser import ParserResultEntry, BadgeException
from .badge_html import generate_badge_html, generate_single_element_badge_html
from .install_badge import InstallBadgeManager
from .tag_badge import TagBadgeManager

LINK_BADGE_EMPTY_FIELDS = ["copy_text", "link", "reflink"]
REFLINK_BADGE_EMPTY_FIELDS = LINK_BADGE_EMPTY_FIELDS
INSTALL_BADGE_EMPTY_FIELDS = LINK_BADGE_EMPTY_FIELDS
COPY_BADGE_EMPTY_FIELDS = LINK_BADGE_EMPTY_FIELDS
TAG_BADGE_EMPTY_FIELDS = LINK_BADGE_EMPTY_FIELDS
STRIP_SUBDOMAINS = [
    "www", # Pretty standard prefix for websites
    "m", # Pretty standard for mobile sites
]

def format_badge(badge_entry: ParserResultEntry, install_badge_manager: InstallBadgeManager, tag_badge_manager: TagBadgeManager) -> str:
    badge = badge_entry.parsed_badge
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
        value = badge.value
        try:
            value = get_simplified_hostname(value)
            link = value
        except Exception:
            LOGGER.warning(f"Failed to parse hostname from link badge value: {value}")
            link = None # The value may not be a link, so we drop it

        classes = ["badge-link", *badge.html_classes]
        return generate_badge_html(badge.title, value, link=link, extra_classes=classes)

    elif typ == "R":
        badge.assert_all_empty(REFLINK_BADGE_EMPTY_FIELDS)
        classes = ["badge-reflink", *badge.html_classes]
        badge_html = generate_badge_html(badge.title, badge.value, extra_classes=classes)
        return f"[{badge_html}][{badge.value}]"

    elif typ == "I":
        return install_badge_manager.format_badge(badge_entry)
    
    elif typ == "C":
        badge.assert_all_empty(COPY_BADGE_EMPTY_FIELDS)
        classes = ["badge-copy", *badge.html_classes]
        return generate_badge_html(badge.title, badge.value, copy_text=badge.value, extra_classes=classes)

    elif typ == "T":
        badge.assert_all_empty(TAG_BADGE_EMPTY_FIELDS)
        return tag_badge_manager.format_badge(badge_entry)

    elif typ == "S":
        classes = ["badge-single", *badge.html_classes]
        badge_html = generate_single_element_badge_html(badge.title, copy_text=badge.copy_text, link=badge.link, extra_classes=classes)
        if badge.reflink:
            badge_html = f"[{badge_html}][{badge.reflink}]"
        return badge_html

    else:
        raise BadgeException(f"Unknown badge type '{typ}'. Known types are '', L, R, I, C, T, S")


def get_simplified_hostname(url: str) -> str:
    url = url.strip()
    simplified_host_name = urlparse(url).netloc
    if not simplified_host_name:
        raise UserWarning(f"No hostname in URL: '{url}'")
    
    # Remove unnecessary subdomains: for example "www.example.com" -> "example.com"
    parts = simplified_host_name.split(".")
    if len(parts) >= 2: # only handle www.example.com, but not www.com
        if parts[0] in STRIP_SUBDOMAINS:
            # remove the first subdomain
            parts = parts[1:]
            # store our change in the original variable
            simplified_host_name = ".".join(parts)
    
    return simplified_host_name

