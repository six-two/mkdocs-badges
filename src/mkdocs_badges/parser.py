#!/usr/bin/env python3
# This parser decides, which lines to parse as badges and extracts the data used to construct the badges
from typing import NamedTuple, Optional
import re
# local files
from . import warning_for_location
from .parsed_badge import ParsedBadge, BadgeException

class ParserResultEntry(NamedTuple):
    file_name: str
    line_index: int
    only_replace_substring: Optional[str] # We set this field if we do a replacement of a table cell (and not the whole line)
    parsed_badge: ParsedBadge

class SplitPart(NamedTuple):
    raw: str # the original string, as it was read
    interpreted: str # this version interprets escaped characters. For example \\ will be a \ and \<SEPARATOR> will be the literal character <SEPARATOR>

# Optional whitespace, optional alignment, at least three dashes, optional alignment, optional whitespace
# Update from #4: It seems to be possible to just use a single dash
TABLE_CELL_REGEX = r"\s*:?-+:?\s*"
TABLE_HEADER_REGEX = re.compile(r"^\s*\|?"+ TABLE_CELL_REGEX + r"(\|" + TABLE_CELL_REGEX + ")+\|?\s*$")

CLASS_ATTR_REGEX = re.compile(r"^(?:\.|(?:class:))(.*)$")
COPY_ATTR_REGEX = re.compile(r"^c(?:opy)?:(.*)$")
LINK_ATTR_REGEX = re.compile(r"^l(?:ink)?:(.*)$")
REF_LINK_ATTR_REGEX = re.compile(r"^r(?:eflink)?:(.*)$")


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
    def __init__(self, file_name: str, file_content_lines: list[str], badge_separator: str, badge_table_separator: str):
        self.file_name = file_name
        # Add an empty line, since for the table header check we need to look ahead one line
        # This is way easier than specialized edge case handling rules
        self.lines = [*file_content_lines, ""]
        self.is_fenced_code_block = False
        self.is_table = False

        self.badge_separator = badge_separator
        self.badge_table_separator = badge_table_separator
        self.escape_character = "\\"

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

        if (not self.is_table) and TABLE_HEADER_REGEX.match(line):
            # This is probably the start of a table. This line should not be processed
            self.is_table = True
            return False

        # If we found no reason not to process the line, we should process it
        return True

    def try_parse_line(self, line: str, index: int) -> Optional[ParserResultEntry]:
        try:
            line = line.rstrip()
            badge_separator = self.badge_table_separator if self.is_table else self.badge_separator

            # Check if the line has pipe "|" symbols at the beginning and ending
            if badge_separator not in line[:2] or line[-1] != badge_separator:
                # Missing pipe symbol, this can not be a badge
                return None

            parts = self.split_by_separator(line, badge_separator)
            # A valid line needs at least three separators (four parts): "|title|value|" -> ["", "title", "value", ""]
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
                interpreted_parts = [x.interpreted for x in parts]
                parsed_badge = parse_badge_parts(interpreted_parts)

                # Return the badge info that we parsed
                return ParserResultEntry(
                    file_name=self.file_name,
                    line_index=index,
                    parsed_badge=parsed_badge,
                    only_replace_substring=None, # will be set outside of this method if required
                )
            except Exception as ex:
                # Parsing failed, let's give some info to help with debugging
                warning_for_location(self.file_name, index, f"Parsing error: {ex}")
                return None

        except BadgeException as ex:
            # General error, probably caused by bad input (like invalid escape seqouence)
            warning_for_location(self.file_name, index, f"General processing error: {ex}")
            return None

    def split_by_separator(self, text: str, separator: str) -> list[SplitPart]:
        result = []
        current_part_raw = ""
        current_part_interpreted = ""
        current_is_escaped = False

        for char in text:
            current_part_raw += char
            if current_is_escaped:
                if char == separator:
                    # Treat the escaped separator as just a normal character
                    current_part_interpreted += char
                elif char == self.escape_character:
                    # keep only one of the backslashes
                    current_part_interpreted += self.escape_character
                else:
                    # We do not understand this escaping, but it may be used to escape markdown characters or something.
                    # So we do not modify it
                    current_part_interpreted += self.escape_character + char
                
                current_is_escaped = False
            else:
                if char == self.escape_character:
                    current_is_escaped = True
                elif char == separator:
                    current_part_raw = current_part_raw[:-1] # remove the separator, which we already have appended
                    result.append(SplitPart(raw=current_part_raw, interpreted=current_part_interpreted))
                    current_part_raw = current_part_interpreted = ""
                else:
                    current_part_interpreted += char
        
        result.append(SplitPart(raw=current_part_raw, interpreted=current_part_interpreted))
        return result

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
                line = self.lines[index]
                if self.is_table:
                    # For a table we try to treat every column as a line, since they all could contain badges
                    try:
                        # We do not do a simple string split, since there may be escaped separators ('\|') in the line
                        for cell in self.split_by_separator(line, "|"):
                            # Allow (ignore) whitespace between table separators and cell contents
                            cell_string = cell.interpreted.strip()
                            # We treat every cell like its own line (the method inside handles not actually replacing the full line later)
                            if result := self.try_parse_line(cell_string, index):
                                # Use the actual read raw data, so that I do not have to undo ambiguous unescaping (caused wierd bugs)
                                result = result._replace(only_replace_substring=cell.raw.strip())
                                results.append(result)
                    except Exception as ex:
                        warning_for_location(self.file_name, index, f"Error splitting table columns in line '{line}': {ex}")
                else:
                    if result := self.try_parse_line(line, index):
                        results.append(result)

        return results
