#!/usr/bin/env python3
# This parser decides, which lines to parse as badges and extracts the data used to construct the badges
from typing import NamedTuple, Optional
import re
# local files
from . import warning

class BadgeException(Exception):
    pass


class ParsedBadge:
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


class ParserResultEntry(NamedTuple):
    line_index: int
    parsed_badge: ParsedBadge

# Optional whitespace, optional alignment, at least three dashes, optional alignment, optional whitespace
# Update from #4: It seems to be possible to just use a single dash
TABLE_CELL_REGEX = r"\s*:?-+:?\s*"
TABLE_HEADER_REGEX = re.compile(r"^\s*\|?"+ TABLE_CELL_REGEX + r"(\|" + TABLE_CELL_REGEX + ")+\|?\s*$")

CLASS_ATTR_REGEX = re.compile(r"^(?:\.|(?:class:))(.*)$")
COPY_ATTR_REGEX = re.compile(r"^c(?:opy)?:(.*)$")
LINK_ATTR_REGEX = re.compile(r"^l(?:ink)?:(.*)$")
REF_LINK_ATTR_REGEX = re.compile(r"^r(?:eflink)?:(.*)$")

# Test string: a|b|c\|d|e\\|f\\\|g\\\\h|\\\\\i|\\\\\\j|k
SEPARATOR = "|"
ESCAPE = "\\"
ALLOWED_ESCAPED_CHARACTERS = [ESCAPE, SEPARATOR]


def split_by_separator(text: str) -> list[str]:
    result = []
    current_part = ""
    current_is_escaped = False

    for char in text:
        if current_is_escaped:
            if char in ALLOWED_ESCAPED_CHARACTERS:
                current_part += char
                current_is_escaped = False
            else:
                pretty_allowed_sequences = ", ".join([f"'{seq}'" for seq in ALLOWED_ESCAPED_CHARACTERS])
                raise BadgeException(f"'{ESCAPE}{char}' is not a valid escape sequence. Allowed escape sequences are {pretty_allowed_sequences}")
        else:
            if char == ESCAPE:
                current_is_escaped = True
            elif char == SEPARATOR:
                result.append(current_part)
                current_part = ""
            else:
                current_part += char
    
    result.append(current_part)
    return result


def parse_badge_parts(parts: list[str]) -> ParsedBadge:
    badge_type = parts[0]
    if len(badge_type) > 1:
        raise BadgeException(f"Badge type needs to have a length <= 1, but is '{badge_type}'")
    copy_text = None
    link = None
    reflink = None
    html_classes = []
    attribute_list = parts[3:-1]

    for attribute in attribute_list:
        if match := CLASS_ATTR_REGEX.match(attribute):
            attr = match.group(1)
            html_classes.append(attr)
        elif match := COPY_ATTR_REGEX.match(attribute):
            if copy_text:
                raise BadgeException("Multiple 'c:' / 'copy:' attributes defined")
            else:
                copy_text = match.group(1)
        elif match := LINK_ATTR_REGEX.match(attribute):
            if link:
                raise BadgeException("Multiple 'l:' / 'link:' attributes defined")
            else:
                link = match.group(1)
        elif match := REF_LINK_ATTR_REGEX.match(attribute):
            if reflink:
                raise BadgeException("Multiple 'r:' / 'reflink:' attributes defined")
            else:
                reflink = match.group(1)
        else:
            raise BadgeException(f"Unknown attribute: '{attribute}'")


    return ParsedBadge(
        badge_type,
        parts[1],
        parts[2],
        copy_text,
        link,
        reflink,
        html_classes,
    )


class FileParser:
    def __init__(self, file_name: str, file_content_lines: list[str]):
        self.file_name = file_name
        # Add an empty line, since for the table header check we need to look ahead one line
        # This is way easier than specialized edge case handling rules
        self.lines = [*file_content_lines, ""]
        self.is_fenced_code_block = False
        self.is_table = False

    def should_process_line(self, index: int) -> bool:
        line = self.lines[index]
        ls_line = line.lstrip()

        if not ls_line:
            # An empty line. Marks the end of a table (if one was open). Should not be processed
            self.is_table = False
            return False

        if ls_line.startswith("```"):
            # This line starts/ends a code block, so it can not contain a badge
            self.is_fenced_code_block = not self.is_fenced_code_block
            return False

        if self.is_fenced_code_block:
            # Do not parse badges in fenced code blocks
            return False

        if ls_line != line:
            # This line is indented (probably a code block). Do not process
            return False

        if TABLE_HEADER_REGEX.match(line):
            # This is probably the start of a table. This line should not be processed
            self.is_table = True
            return False

        if self.is_table:
            # If we are in a table, we do not process badges
            return False

        # If we found no reason not to process the line, we should process it
        return True

    def try_parse_line(self, index: int) -> Optional[ParserResultEntry]:
        try:
            line = self.lines[index]
            line = line.rstrip()

            # Check if the line has pipe "|" symbols at the beginning and ending
            if "|" not in line[:2] or line[-1] != "|":
                # Missing pipe symbol, this can not be a badge
                return None

            parts = split_by_separator(line)
            # A valid line needs at least three pipes (four parts): "|title|value|" -> ["", "title", "value", ""]
            if len(parts) < 4:
                # This can not be a valid badge, since it has to few parts
                return None

            # Check if the next line is a table header indicator
            next_line = self.lines[index + 1]
            if TABLE_HEADER_REGEX.match(next_line):
                # This line is probably the table header, so we do not try to parse it
                return None
            
            # This is not a table header, so let's try parsing it
            try:
                parsed_badge = parse_badge_parts(parts)
                # Return the badge info that we parsed
                return ParserResultEntry(
                    line_index=index,
                    parsed_badge=parsed_badge,
                )
            except Exception as ex:
                # Parsing failed, let's give some info to help with debugging
                warning(f"[{self.file_name}:{index+1}] Parsing error: {ex}")
                return None

        except BadgeException as ex:
            # General error, probably caused by bad input (like invalid escape seqouence)
            warning(f"[{self.file_name}:{index+1}] General processing error: {ex}")
            return None

    def process(self) -> list[ParserResultEntry]:
        """
        Process the lines of the file and return the line numbers and parsed data of the found badges.
        Should only be called once, since instance variables are not reset!
        """
        results = []
        # Subtract one, since we added the empty line in the constructor
        real_line_count = len(self.lines) - 1
        for index in range(real_line_count):
            # Check if we should try to process the line
            if self.should_process_line(index):
                # Actually try to process the line
                if result := self.try_parse_line(index):
                    # It worked :)
                    results.append(result)

        return results
