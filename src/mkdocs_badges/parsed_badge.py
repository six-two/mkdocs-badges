from typing import NamedTuple, Optional
import re
# local files
from . import warning

class BadgeException(Exception):
    pass


class ParsedBadge:
    """
    This is the object returned by the badge parser in 'parser.py'
    """
    def __init__(
            self,
            badge_type: Optional[str],
            title: str,
            value: str,
            copy_text: Optional[str],
            link: Optional[str],
            reflink: Optional[str],
            html_classes: list[str],
        ):
        # Use the "or None" statements to make sure that the values are really None and not just "". Otherwise two equal seeming objects may not be equal
        self.badge_type = badge_type or None
        # It would look starnge with leading/trailing whitespace
        self.title = title.strip()
        self.value = value.strip()
        self.copy_text = copy_text or None
        self.link = link or None
        self.reflink = reflink or None
        # Sort the class names to make equality checks easier
        self.html_classes = list(sorted(html_classes or []))

    def check_fields(self) -> None:
        if self.badge_type == "S":
            # Special case handling of single value badges, which only contain either a title or a value
            if self.title and self.value:
                raise BadgeException("Single value badges can not contain both a title and a value")
            elif not self.title and not self.value:
                raise BadgeException("Single value batch needs to contain either a title or a value")

            # Normalize values: store data in title, leave value empty
            self.title = self.title or self.value
            self.value = ""

            # Check for other mutually exclusive attributes
            if self.copy_text and (self.link or self.reflink):
                raise BadgeException("Single value badges can not contain both a link and a text to copy")

        else:
            # Normal badges, should contain both title and value
            if not self.title:
                raise BadgeException("No title set")
            if not self.value:
                raise BadgeException("No value set")
        
        if self.link and self.reflink:
            raise BadgeException("Mutually exclusive fields 'link' and 'reflink' set")

    def assert_empty(self, name: str) -> None:
        value = self.__dict__.get(name, None)
        if value:
            raise BadgeException(f"Expected empty value for field '{name}', but got {repr(value)}")

    def assert_all_empty(self, name_list: list[str]) -> None:
        for name in name_list:
            self.assert_empty(name)

    def __repr__(self) -> str:
        parts = [
            self.badge_type or "",
            self.title,
            self.value,
        ]
        if self.copy_text:
            parts.append(f"c:{self.copy_text}")
        if self.link:
            parts.append(f"l:{self.link}")
        if self.reflink:
            parts.append(f"r:{self.reflink}")
        if self.html_classes:
            parts += self.html_classes

        return f"<ParsedBadge:{parts}>"

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return (self.badge_type == other.badge_type
                and self.title == other.title
                and self.value == other.value
                and self.copy_text == other.copy_text
                and self.link == other.link
                and self.reflink == other.reflink
                and self.html_classes == other.html_classes)
        else:
            return False
