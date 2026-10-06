import unittest

from src.main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_h1(self):
        self.assertEqual(extract_title("# My Title"), "My Title")

    def test_h1_with_extra_padding_is_stripped(self):
        self.assertEqual(extract_title("#   Padded Title  "), "Padded Title")

    def test_h1_inside_full_document(self):
        markdown = """Some intro paragraph.

# Real Title

Follow-up paragraph with **bold** text."""
        self.assertEqual(extract_title(markdown), "Real Title")

    def test_no_heading_raises_value_error(self):
        with self.assertRaises(ValueError):
            extract_title("plain text only\nmore plain text")

    def test_empty_string_raises_value_error(self):
        with self.assertRaises(ValueError):
            extract_title("")

    def test_first_h1_wins_with_multiple_h1s(self):
        markdown = "# First Title\n\nparagraph\n\n# Second Title"
        self.assertEqual(extract_title(markdown), "First Title")

    # NOTE: prompt claimed these two cases hit a known bug
    # (implementation matching any line starting with "#"), but the
    # current source checks `startswith("# ")` — the bug is already
    # fixed, so these are plain passing tests.

    def test_h2_before_h1_returns_h1(self):
        markdown = "## Subtitle\n# Real Title"
        self.assertEqual(extract_title(markdown), "Real Title")

    def test_hashtag_without_space_is_not_a_title(self):
        with self.assertRaises(ValueError):
            extract_title("#hashtag line\nplain text")


if __name__ == "__main__":
    unittest.main()
