import html
import json
import re
from typing import NamedTuple, Optional
# pip
from mkdocs.structure.pages import Page
# local files
from . import warning
from .badge_html import generate_badge_html
from .parser import ParsedBadge

TAG_REGEX_BAD_CHARS = re.compile("[^0-9a-zA-Z_]+")
TAG_REGEX_MULTI_UNDERSCORES = re.compile("__+")


def get_tag_name(title: str, value: str) -> str:
    tag_name = f"{title}_{value}".lower()
    # Replace all non-alpha-numeric with underscores
    tag_name = TAG_REGEX_BAD_CHARS.sub("_", tag_name)
    # Remove double underscores
    tag_name = TAG_REGEX_MULTI_UNDERSCORES.sub("_", tag_name)

    # remove loading / trailing underscores
    if tag_name.startswith("_"):
        tag_name = tag_name[1:]
    if tag_name.endswith("_"):
        tag_name = tag_name[:-1]
    return tag_name


class TagBadgeManager:
    def __init__(self, tag_page_link: str) -> None:
        self.tag_page_link = tag_page_link
        self.tags = set()

    def apply_tags_to_page(self, page: Page) -> None:
        """
        This adds the tags to the given page and clear the lost of stored tags afterwards (so that you can reuse the object)
        """
        if self.tags:
            warning("Debug:")
            # Get the new tags
            new_tags = sorted(list(self.tags))

            # Update the page's tags
            tags = page.meta.get("tags", [])
            tags += new_tags
            page.meta["tags"] = tags

            # Empty tag list
            self.tags = set()

    def format_badge(self, badge: ParsedBadge) -> str:
        tag_name = get_tag_name(badge.title, badge.value)
        classes = ["badge-tag", *badge.html_classes]
        link = f"{self.tag_page_link}#{tag_name}"

        self.tags.add(tag_name)
        return generate_badge_html(badge.title, badge.value, link=link, extra_classes=classes)
