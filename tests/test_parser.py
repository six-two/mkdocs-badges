#!/usr/bin/env python3
import unittest
from mkdocs_badges.parser import BadgeException, FileParser, ParsedBadge, ParserResultEntry

BADGE_SEPARATOR = "|"
BADGE_TABLE_SEPARATOR = "^"
FILE_NAME = "TestFileParser"
INLINE_BADGE_START = "["
INLINE_BADGE_END = "]"

def parse_lines(lines: list[str]):
    return FileParser(FILE_NAME, lines, BADGE_SEPARATOR, BADGE_TABLE_SEPARATOR, INLINE_BADGE_START, INLINE_BADGE_END).process()


class TestFileParser(unittest.TestCase):

    def test_badge_simple(self):
        results = parse_lines(["|title|value|"])

        expected_results = [
            ParserResultEntry(
                file_name=FILE_NAME,
                line_index=0,
                only_replace_substring=None,
                parsed_badge=ParsedBadge(None, "title", "value", None, None, None, []),
                replace_characters_before_html_output=[],
            )
        ]
        self.assertEqual(results, expected_results)

    def test_badge_install(self):
        results = parse_lines(["I|pypi|mkdocs-badges|"])

        expected_results = [
            ParserResultEntry(
                file_name=FILE_NAME,
                line_index=0,
                parsed_badge=ParsedBadge("I", "pypi", "mkdocs-badges", None, None, None, []),
                only_replace_substring=None,
                replace_characters_before_html_output=[],
            )
        ]
        self.assertEqual(results, expected_results)

    def test_badge_type_unknown(self):
        results = parse_lines(["X|title|value|"])

        expected_results = [
            ParserResultEntry(
                file_name=FILE_NAME,
                line_index=0,
                parsed_badge=ParsedBadge("X", "title", "value", None, None, None, []),
                only_replace_substring=None,
                replace_characters_before_html_output=[],
            )
        ]
        self.assertEqual(results, expected_results)

    def test_badge_no_trailing_pipe(self):
        results = parse_lines(["X|title|value"])

        expected_results = []
        self.assertEqual(results, expected_results)

    def test_badge_table_header(self):
        results = parse_lines(["|---|---|"])

        expected_results = []
        self.assertEqual(results, expected_results)

    def test_badge_in_table(self):
        results = parse_lines(["|A|B|", "|---|---|", "|a|b|", "|c|d|"])

        expected_results = []
        self.assertEqual(results, expected_results)

    def test_badge_after_table(self):
        results = parse_lines(["|A|B|", "|---|---|", "|a|b|", "|c|d|", "", "|title|value|"])

        expected_results = [
            ParserResultEntry(
                file_name=FILE_NAME,
                line_index=5,
                parsed_badge=ParsedBadge("", "title", "value", None, None, None, []),
                only_replace_substring=None,
                replace_characters_before_html_output=[],
            )
        ]
        self.assertEqual(results, expected_results)


    def test_badge_type_too_long(self):
        results = parse_lines(["XYZ|title|value|"])

        expected_results = []
        self.assertEqual(results, expected_results)

    def test_badge_with_escaped_pipes(self):
        results = parse_lines([r"|title\|\\|value|"])

        expected_results = [
            ParserResultEntry(
                file_name=FILE_NAME,
                line_index=0,
                parsed_badge=ParsedBadge("", "title|\\", "value", None, None, None, []),
                only_replace_substring=None,
                replace_characters_before_html_output=[],
            )
        ]
        self.assertEqual(results, expected_results)



if __name__ == "__main__":
    unittest.main()