# local files
from . import warning_for_entry, LOGGER
from .parser import ParserResultEntry, BadgeException, FileParser
from .formatter import format_badge

BADGE_GROUP_START = '<span class="badge-group">'
BADGE_GROUP_END = '</span>'

def replace_badges(file_name: str, markdown: str, badge_separator: str, badge_table_separator: str, *args) -> str:
    lines = markdown.split("\n")

    parser_result_list = FileParser(file_name, lines, badge_separator, badge_table_separator).process()
    if parser_result_list:
        return BadgeReplacer().get_replaced_markdown(lines, parser_result_list, *args)
    else:
        return markdown


def group_entries_by_line(parser_result_list: list[ParserResultEntry]) -> dict[int,list[ParserResultEntry]]:
    replacements_by_line_index: dict[int,list[ParserResultEntry]] = {}
    for entry in parser_result_list:
        try:
            replacements_by_line_index[entry.line_index].append(entry)
        except KeyError:
            replacements_by_line_index[entry.line_index] = [entry]
    return replacements_by_line_index

class BadgeReplacer:
    def get_replaced_markdown(self, lines: list[str], parser_result_list: list[ParserResultEntry], *args):
        self.lines = lines
        # This is to track entirely replaced lines
        self.replaced_line_indices: list[int] = []
        for line_number, entry_list in group_entries_by_line(parser_result_list).items():
            self.process_badges_for_line(line_number, entry_list, *args)
        
        self.insert_group_spans_for_adjacent_lines()
        return "\n".join(self.lines)

    def process_badges_for_line(self, line_number: int, entry_list: list[ParserResultEntry], *args) -> None:
        self.line = self.lines[line_number]
        self.badge_groups: list[tuple[int,int]] = []
        self.badge_group_start = -1
        self.last_badge_end = -1
        self.badge_group_size = 0
        self.line_number = line_number

        for entry in entry_list:
            try:
                self.process_parser_entry(entry, *args)
            except BadgeException as error:
                warning_for_entry(entry, f"Processing error: {error}")
        
        self.insert_group_span_in_current_line()
        # Finally store the modified line
        self.lines[line_number] = self.line

    def process_parser_entry(self, entry: ParserResultEntry, *args):
        badge_html = format_badge(entry, *args)
        # depending on where the badge is from, we need to escape some characters (like '|' in tables)
        for old, new in entry.replace_characters_before_html_output:
            badge_html = badge_html.replace(old, new)
        
        if entry.only_replace_substring:
            self.do_inline_badge_replace(entry, badge_html)
        else:
            # Just replace the entire line
            self.line = badge_html

    def do_inline_badge_replace(self, entry: ParserResultEntry, badge_html: str) -> None:
        try:
            if not entry.only_replace_substring:
                LOGGER.warning("Bug: only_replace_substring is not set")
                return
            else:
                current_start = self.line.index(entry.only_replace_substring)
        except ValueError:
            # Handle cases where we did not find the substring
            warning_for_entry(entry, f"badge_replacer::replace_badges: Failed to find '{entry.only_replace_substring}' in line:\n{self.line}\nBefore any replacements the line was:\n{self.lines[self.line_number]}")
            return

        # Check if there is only white space between the end of the last badge and the start of this one
        if self.badge_group_start == -1 or self.line[self.last_badge_end:current_start].strip():
            # Not just white space, end the previous group
            if self.badge_group_size > 1:
                self.badge_groups.append((self.badge_group_start, self.last_badge_end))

            # Start a new badge group
            self.badge_group_start = current_start
            self.badge_group_size = 1
        else:
            # Continue the current group
            self.badge_group_size += 1

        self.last_badge_end = current_start + len(badge_html)
        # replace original badge syntax with HTML
        end_index_in_original_line = current_start + len(entry.only_replace_substring)
        self.line = self.line[:current_start] + badge_html + self.line[end_index_in_original_line:]

    def insert_group_span_in_current_line(self):
        # After the last badge, close any open groups
        if self.badge_group_size > 1:
            self.badge_groups.append((self.badge_group_start, self.last_badge_end))

        # Handle in reverse order, so that the indices remain correct
        for group_start, group_end in reversed(self.badge_groups):
            # print(f"Debug: Inline badge group: line {line_number}, start {group_start}, end {group_end}")
            self.line = self.line[:group_start] + BADGE_GROUP_START + self.line[group_start:group_end] + BADGE_GROUP_END + self.line[group_end:]

    def insert_group_spans_for_adjacent_lines(self):
        # Surround each group of badges (whole lines) with the container placeholders (required for layout)
        self.replaced_line_indices = list(sorted(self.replaced_line_indices))
        last_i = len(self.replaced_line_indices) - 1
        for i, line in enumerate(self.replaced_line_indices):
            # is first entry or is not consecutive line to previous line
            if (i == 0) or (self.replaced_line_indices[i-1] != line - 1):
                self.lines[line] = BADGE_GROUP_START + self.lines[line]

            # is last or the next line is not consecutive
            if (i == last_i) or (self.replaced_line_indices[i+1] != line + 1):
                self.lines[line] += BADGE_GROUP_END

