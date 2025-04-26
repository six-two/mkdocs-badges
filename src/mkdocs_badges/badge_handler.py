from urllib.parse import urlparse

# local files
from . import warning_for_entry, LOGGER
from .parser import ParserResultEntry, BadgeException, FileParser
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
# > Sadly I can not put the HTML in directly, because then the reference link markdown would not be parsed.
# > So I insert a placeholder, let the markdown parser convert the reference links, and then replace the placeholders with the true HTML
# Actually the problem described above can be circumvented by simply using a span instead of a div
BADGE_GROUP_START = '<span class="badge-group">'
BADGE_GROUP_END = '</span>'


def replace_badges(file_name: str, markdown: str, badge_separator: str, badge_table_separator: str, *args) -> str:
    lines = markdown.split("\n")

    parser_result_list = FileParser(file_name, lines, badge_separator, badge_table_separator).process()
    if parser_result_list:
        # This is to track entirely replaced lines
        replaced_line_indices = []

        replacements_by_line_index: dict[int,list[ParserResultEntry]] = {}
        for entry in parser_result_list:
            try:
                replacements_by_line_index[entry.line_index].append(entry)
            except KeyError:
                replacements_by_line_index[entry.line_index] = [entry]

        # We need this mess if we want to group inline badges. Unless someone has a simpler idea
        for line_number, entry_list in replacements_by_line_index.items():
            # lets assume, that all badges are in the correct order
            line = lines[line_number]
            if len(entry_list) == 1:
                entry = entry_list[0]
                try:
                    badge_html = format_badge(entry, *args)
                    # Indent it a bit to make debugging it easier when viewing the page's source

                    # depending on where the badge is from, we need to escape some characters (like '|' in tables)
                    for old, new in entry.replace_characters_before_html_output:
                        badge_html = badge_html.replace(old, new)

                    if entry.only_replace_substring:
                        # Replace only part of the line (for table cells)
                        old_line = lines[entry.line_index]
                        new_line = old_line.replace(entry.only_replace_substring, badge_html)
                        if old_line != new_line:
                            lines[entry.line_index] = new_line
                        else:
                            warning_for_entry(entry, f"Replacing '{entry.only_replace_substring}' in line '{old_line}' failed")
                    else:
                        # Replaced the entire line
                        lines[entry.line_index] = f"\t{badge_html}"
                        replaced_line_indices.append(entry.line_index)
                except BadgeException as error:
                    warning_for_entry(entry, f"Processing error: {error}")
            else:
                badge_groups = []
                badge_group_start = -1
                last_badge_end = -1
                badge_group_size = 0
                for entry in entry_list:
                    try:
                        badge_html = format_badge(entry, *args)
                        # depending on where the badge is from, we need to escape some characters (like '|' in tables)
                        for old, new in entry.replace_characters_before_html_output:
                            badge_html = badge_html.replace(old, new)

                        if entry.only_replace_substring:
                            try:
                                current_start = line.index(entry.only_replace_substring)
                            except ValueError:
                                # Handle cases where we did not find the substring
                                warning_for_entry(entry, f"badge_handler::replace_badges: Failed to find '{entry.only_replace_substring}' in line:\n{line}\nBefore any replacements the line was:\n{lines[line_number]}")
                                continue

                            # Check if there is only white space between the end of the last badge and the start of this one
                            if badge_group_start == -1 or line[last_badge_end:current_start].strip():
                                # Not just white space, end the previous group
                                if badge_group_size > 1:
                                    badge_groups.append((badge_group_start, last_badge_end))

                                # Start a new badge group
                                badge_group_start = current_start
                                badge_group_size = 1
                            else:
                                # Continue the current group
                                badge_group_size += 1

                            last_badge_end = current_start + len(badge_html)
                            # replace original badge syntax with HTML
                            end_index_in_original_line = current_start + len(entry.only_replace_substring)
                            line = line[:current_start] + badge_html + line[end_index_in_original_line:]
                        else:
                            warning_for_entry(entry, "BUG: There are multiple badges in a line, but it also claims that the whole line is a badge. This is mutually exclusive.")
                    except BadgeException as error:
                        warning_for_entry(entry, f"Processing error: {error}")
                
                # After the last badge, close any open groups
                if badge_group_size > 1:
                    badge_groups.append((badge_group_start, last_badge_end))

                # Handle in reverse order, so that the indices remain correct
                for group_start, group_end in reversed(badge_groups):
                    # print(f"Debug: Inline badge group: line {line_number}, start {group_start}, end {group_end}")
                    line = line[:group_start] + BADGE_GROUP_START + line[group_start:group_end] + BADGE_GROUP_END + line[group_end:]

                # Finally store the modified line
                lines[line_number] = line

        # Surround each group of badges (whole lines) with the container placeholders (required for layout)
        replaced_line_indices = list(sorted(replaced_line_indices))
        last_i = len(replaced_line_indices) - 1
        for i, line in enumerate(replaced_line_indices):
            # is first entry or is not consecutive line to previous line
            if (i == 0) or (replaced_line_indices[i-1] != line - 1):
                lines[line] = BADGE_GROUP_START + lines[line]

            # is last or the next line is not consecutive
            if (i == last_i) or (replaced_line_indices[i+1] != line + 1):
                lines[line] += BADGE_GROUP_END

        return "\n".join(lines)
    else:
        return markdown


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

