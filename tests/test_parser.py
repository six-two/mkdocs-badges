#!/usr/bin/env python3
import unittest
from mkdocs_badges.parser import BadgeException, FileParser, ParsedBadge, ParserResultEntry

class TestFileParser(unittest.TestCase):
    def test_badge_simple(self):
        results = FileParser("TestFileParser", ["|title|value|"]).process()

        expected_results = [
            ParserResultEntry(
                line_index=0,
                parsed_badge=ParsedBadge(None, "title", "value", None, None, None, []),
            )
        ]
        self.assertEqual(results, expected_results)

    def test_badge_install(self):
        results = FileParser("TestFileParser", ["I|pypi|mkdocs-badges|"]).process()

        expected_results = [
            ParserResultEntry(
                line_index=0,
                parsed_badge=ParsedBadge("I", "pypi", "mkdocs-badges", None, None, None, []),
            )
        ]
        self.assertEqual(results, expected_results)

    def test_badge_type_unknown(self):
        results = FileParser("TestFileParser", ["X|title|value|"]).process()

        expected_results = [
            ParserResultEntry(
                line_index=0,
                parsed_badge=ParsedBadge("X", "title", "value", None, None, None, []),
            )
        ]
        self.assertEqual(results, expected_results)

    def test_badge_with_escaped_pipes(self):
        results = FileParser("TestFileParser", [r"|title\|\\|value|"]).process()

        expected_results = [
            ParserResultEntry(
                line_index=0,
                parsed_badge=ParsedBadge("", "title|\\", "value", None, None, None, []),
            )
        ]
        self.assertEqual(results, expected_results)



if __name__ == "__main__":
    unittest.main()