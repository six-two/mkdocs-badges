#!/usr/bin/env python3
import unittest
from mkdocs_badges.parser import BadgeException, FileParser, ParsedBadge, ParserResultEntry

BADGE_SEPARATOR = "|"
BADGE_TABLE_SEPARATOR = "^"
FILE_NAME = "TestFileParser"

class TestFileParser(unittest.TestCase):
    def test_badge_simple(self):
        results = FileParser(FILE_NAME, ["|title|value|"], BADGE_SEPARATOR, BADGE_TABLE_SEPARATOR).process()

        expected_results = [
            ParserResultEntry(
                file_name=FILE_NAME,
                line_index=0,
                parsed_badge=ParsedBadge(None, "title", "value", None, None, None, []),
                only_replace_substring=None,
            )
        ]
        self.assertEqual(results, expected_results)

    def test_badge_install(self):
        results = FileParser(FILE_NAME, ["I|pypi|mkdocs-badges|"], BADGE_SEPARATOR, BADGE_TABLE_SEPARATOR).process()

        expected_results = [
            ParserResultEntry(
                file_name=FILE_NAME,
                line_index=0,
                parsed_badge=ParsedBadge("I", "pypi", "mkdocs-badges", None, None, None, []),
                only_replace_substring=None,
            )
        ]
        self.assertEqual(results, expected_results)

    def test_badge_type_unknown(self):
        results = FileParser(FILE_NAME, ["X|title|value|"], BADGE_SEPARATOR, BADGE_TABLE_SEPARATOR).process()

        expected_results = [
            ParserResultEntry(
                file_name=FILE_NAME,
                line_index=0,
                parsed_badge=ParsedBadge("X", "title", "value", None, None, None, []),
                only_replace_substring=None,
            )
        ]
        self.assertEqual(results, expected_results)

    def test_badge_no_trailing_pipe(self):
        results = FileParser(FILE_NAME, ["X|title|value"], BADGE_SEPARATOR, BADGE_TABLE_SEPARATOR).process()

        expected_results = []
        self.assertEqual(results, expected_results)

    def test_badge_table_header(self):
        results = FileParser(FILE_NAME, ["|---|---|"], BADGE_SEPARATOR, BADGE_TABLE_SEPARATOR).process()

        expected_results = []
        self.assertEqual(results, expected_results)

    def test_badge_in_table(self):
        results = FileParser(FILE_NAME, ["|A|B|", "|---|---|", "|a|b|", "|c|d|"], BADGE_SEPARATOR, BADGE_TABLE_SEPARATOR).process()

        expected_results = []
        self.assertEqual(results, expected_results)

    def test_badge_after_table(self):
        results = FileParser(FILE_NAME, ["|A|B|", "|---|---|", "|a|b|", "|c|d|", "", "|title|value|"], BADGE_SEPARATOR, BADGE_TABLE_SEPARATOR).process()

        expected_results = [
            ParserResultEntry(
                file_name=FILE_NAME,
                line_index=5,
                parsed_badge=ParsedBadge("", "title", "value", None, None, None, []),
                only_replace_substring=None,
            )
        ]
        self.assertEqual(results, expected_results)


    def test_badge_type_too_long(self):
        results = FileParser(FILE_NAME, ["XYZ|title|value|"], BADGE_SEPARATOR, BADGE_TABLE_SEPARATOR).process()

        expected_results = []
        self.assertEqual(results, expected_results)

    def test_badge_with_escaped_pipes(self):
        results = FileParser(FILE_NAME, [r"|title\|\\|value|"], BADGE_SEPARATOR, BADGE_TABLE_SEPARATOR).process()

        expected_results = [
            ParserResultEntry(
                file_name=FILE_NAME,
                line_index=0,
                parsed_badge=ParsedBadge("", "title|\\", "value", None, None, None, []),
                only_replace_substring=None,
            )
        ]
        self.assertEqual(results, expected_results)



if __name__ == "__main__":
    unittest.main()