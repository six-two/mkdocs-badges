#!/usr/bin/env python3
# This parser decides, which lines to parse as badges and extracts the data used to construct the badges
from typing import NamedTuple, Optional
import re

class ParsedBadge(NamedTuple):
    badge_type: Optional[str]
    title: str
    value: str
    copy_text: Optional[str]
    link: Optional[str]
    html_classes: list[str]

class ParserResultEntry(NamedTuple):
    line_index: int
    parsed_badge: ParsedBadge

TABLE_CELL_REGEX = r"\s*:?---+:?\s*" # Optional whitespace, optional alignment, at least three dashes, optional alignment, optional whitespace
TABLE_HEADER_REGEX = re.compile(r"^\s*\|?"+ TABLE_CELL_REGEX + r"(\|" + TABLE_CELL_REGEX + ")+\|?\s*$")

CLASS_ATTR_REGEX = re.compile(r"^(?:\.|(?:class:))(.*)$")
COPY_ATTR_REGEX = re.compile(r"^c(?:opy)?:(.*)$")
LINK_ATTR_REGEX = re.compile(r"^l(?:ink)?:(.*)$")

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
                raise Exception(f"'{ESCAPE}{char}' is not a valid escape sequence. Allowed escape sequences are {pretty_allowed_sequences}")
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
        raise Exception(f"Rejected '{badge_type}'. Badge type needs to have a length of 1 or be empty")
    copy_text = None
    link = None
    html_classes = []
    attribute_list = parts[3:-1]

    for attribute in attribute_list:
        if match := CLASS_ATTR_REGEX.match(attribute):
            attr = match.group(1)
            html_classes.append(attr)
        elif match := COPY_ATTR_REGEX.match(attribute):
            if copy_text:
                raise Exception("Multiple 'c:' / 'copy:' attributes defined")
            else:
                copy_text = match.group(1)
                print("c:",copy_text)
        elif match := LINK_ATTR_REGEX.match(attribute):
            if link:
                raise Exception("Multiple 'l:' / 'link:' attributes defined")
            else:
                link = match.group(1)
                print("l:",link)
        else:
            raise Exception(f"Unknown attribute: '{attribute}'")


    return ParsedBadge(
        badge_type=badge_type,
        title=parts[1],
        value=parts[2],
        copy_text= copy_text,
        link=link,
        html_classes=html_classes,
    )


# This is a mess. TODO: rewrite
def parse_file(lines: list[str]) -> list[ParserResultEntry]:
    """
    Parses a set of lines. Returns a list of all badges found.
    """
    # add an empty line at the end to allow the last line to be parsed correctly
    lines = [*lines, ""]
    is_fenced_code_block = False
    is_table = False
    results = []
    # TODO: do proper checks for a markdown table (for example store clumns count and check header line)
    # if the last line is a possible badge, this will store them
    # This behavior is required to handle tables, since the first line may be the start of a table or a badge
    last_line_parts = []
    
    for line_index, line in enumerate(lines):
        ls_line = line.lstrip()
        ignore_line = False

        # Do not proccess lines with leading whitespace
        if ls_line != line:
            ignore_line = True
        # Check for code block
        elif ls_line.startswith("```"):
            is_fenced_code_block = not is_fenced_code_block
            ignore_line = True

        # Watch for the ---|--- line of a table. If found, the previous line is ignored, since it is actually table columns
        if not is_fenced_code_block and TABLE_HEADER_REGEX.match(line):
            is_table = True
            last_line_parts = []
            ignore_line = True

        # watch for the table ending
        if ls_line == "":
            is_table = False

        if last_line_parts:
            try:
                parsed_badge = parse_badge_parts(last_line_parts)
                entry = ParserResultEntry(
                    line_index=line_index-1,
                    parsed_badge=parsed_badge
                )
                results.append(entry)
            except Exception as ex:
                print("error parsing badge:", ex)
                pass
            last_line_parts = []

        if not ignore_line and not is_fenced_code_block and not is_table:
            parts = split_by_separator(line.rstrip())
            # At least three separators. Line ends with separator
            if len(parts) >= 4 and parts[-1] == "":
                last_line_parts = parts
            
    return results


if __name__ == "__main__":
    print("table header regex:", TABLE_HEADER_REGEX.pattern, "\n")
    test_str = r"a|b|c\|d|e\\|f\\\|g\\\\|h\\\\\|i\\\\\\|j"
    print(test_str, "->", "['"+"', '".join(split_by_separator(test_str))+"']")

    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("file", help="the file to parse")
    args = ap.parse_args()

    with open(args.file, "r") as f:
        lines = f.readlines()
        for line_index, parsed in parse_file(lines):
            print(f"\nLine {line_index+1}: '{lines[line_index][:-1]}'")
            print(parsed)
