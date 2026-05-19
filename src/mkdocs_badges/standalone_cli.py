import argparse
import os
import traceback
from typing import NamedTuple
# local files
from . import warning, disable_warnings
from .install_badge import InstallBadgeManager
from .assets import BADGE_CSS, BADGE_JS, INSTALL_BADGE_DATA, copy_asset_if_target_file_does_not_exist
from .badge_replacer import replace_badges
from .tag_badge import TagBadgeManager

DEFAULT_BADGE_CSS_PATH = "assets/stylesheets/badge.css"
DEFAULT_BADGE_JS_PATH = "assets/javascripts/badge.js"


def exit_with_message(msg):
    print(msg)
    exit(1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", "-d", default=".", help="directory containing your markdown (or HTML) files (default: '.')")
    # Settings
    ap.add_argument("--install-badge-data", "-I", default="", help="path to file with additional install badge data")
    ap.add_argument("--tag-page-link", "-T", default="/index.html", help="URL of the tag page (for tag badges, default: '/index.html')")
    # ap.add_argument("--disable-warnings", "-q", action="store_true", help="don't print warnings about malformed badges")
    ap.add_argument("--copy-resources", "-c", action="store_true", help="copy the javascript and CSS files")
    ap.add_argument("--separator", "-b", default="|", help="badge element separator (default: '|')")
    ap.add_argument("--table-separator", "-t", default="^", help="badge separator for badges in table cells (default: '^')")
    ap.add_argument("--inline-badge-start", "-s", default="[", help="start string for inline badges (defaukt: '[')")
    ap.add_argument("--inline-badge-end", "-e", default="]", help="end string for inline badges (default: ']')")
    ap.add_argument("--ignore-lines-starting-with-whitespace", "-l", action="store_true", help="ignore lines starting with whitespace")
    ap.add_argument("--file-encoding", "-E", default="utf-8", help="file encoding to read and write the markdown files (default: 'utf-8')")
    args = ap.parse_args()

    config = StandaloneConfig(
        install_badge_data=args.install_badge_data,
        tag_page_link=args.tag_page_link,
        # disable_warnings=args.disable_warnings,
        separator=args.separator,
        table_separator=args.table_separator,
        inline_badge_start=args.inline_badge_start,
        inline_badge_end=args.inline_badge_end,
        ignore_lines_starting_with_whitespace=args.ignore_lines_starting_with_whitespace,
        copy_resources=args.copy_resources,
        file_encoding=args.file_encoding,
    )

    # @TODO: Is there a way to not have to duplicate this validation (duplicate of plugin.py)
    if len(config.separator) != 1:
        exit_with_message(f"The 'separator' field needs to contain a single character, but has {len(config.separator)}: '{config.separator}'")

    if len(config.table_separator) != 1:
        exit_with_message(f"The 'table_separator' field needs to contain a single character, but has {len(config.table_separator)}: '{config.table_separator}'")

    if config.table_separator == "|":
        exit_with_message("The 'table_separator' field is not allowed to be '|', since that character conflicts with Markdown's table syntax")

    install_badge_manager = InstallBadgeManager()
    # load the defaults
    install_badge_manager.load_badge_templates_from_file(INSTALL_BADGE_DATA)
    if config.install_badge_data:
        # Add new badge data or overwrite default definitions
        install_badge_manager.load_badge_templates_from_file(config.install_badge_data)

    tag_badge_manager = TagBadgeManager(config.tag_page_link)

    docs_dir = args.docs
    for dirpath, dir_names, file_names in os.walk(docs_dir):
        for file_name in file_names:
            if file_name.lower().split(".")[-1] in ["md", "html", "htm"]:
                file_path = os.path.join(dirpath, file_name)
                try:
                    with open(file_path, encoding=config.file_encoding) as f:
                        og_markdown = markdown = f.read()

                    markdown = replace_badges(file_path, markdown, config.separator, config.table_separator, config.inline_badge_start, config.inline_badge_end, config.ignore_lines_starting_with_whitespace, install_badge_manager, tag_badge_manager)
                    # tag_badge_manager.apply_tags_to_page(page) # @TODO maybe: write tags to metadata?

                    if markdown != og_markdown:
                        print(f"Modified: {file_path}")
                        with open(file_path, "w", encoding=config.file_encoding) as f:
                            f.write(markdown)
                except UnicodeDecodeError as ex:
                    print(f"Error reading file '{file_path}' with encoding '{config.file_encoding}'. Please make sure to specify the correct encoding with the --encoding flag.")
                    print("Original error:", ex)
                except Exception:
                    print(f"Error processing '{file_path}'")
                    traceback.print_exc()

    if args.copy_resources:
        copy_asset_if_target_file_does_not_exist(docs_dir, DEFAULT_BADGE_CSS_PATH, BADGE_CSS)
        copy_asset_if_target_file_does_not_exist(docs_dir, DEFAULT_BADGE_JS_PATH, BADGE_JS)
        print(f"\nRemember to add '{DEFAULT_BADGE_CSS_PATH}' as extra_css and '{DEFAULT_BADGE_JS_PATH}' as extra_javascript")


class StandaloneConfig(NamedTuple):
    install_badge_data: str
    tag_page_link: str
    # disable_warnings: bool
    separator: str
    table_separator: str
    inline_badge_start: str
    inline_badge_end: str
    ignore_lines_starting_with_whitespace: bool
    copy_resources: bool
    file_encoding: str

