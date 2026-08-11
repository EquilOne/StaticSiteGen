import unittest

from src.blocks import markdown_to_blocks


class TestBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        blocks = markdown_to_blocks(markdown)
        self.assertListEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_empty_markdown_returns_no_blocks(self):
        self.assertListEqual(markdown_to_blocks(""), [])

    def test_whitespace_only_blocks_are_dropped(self):
        self.assertListEqual(markdown_to_blocks(" \t\n\n  \t"), [])

    def test_multiple_consecutive_blank_lines_do_not_create_empty_blocks(self):
        self.assertListEqual(markdown_to_blocks("first\n\n\n\nsecond"), ["first", "second"])

    def test_surrounding_spaces_and_tabs_are_stripped(self):
        markdown = "\t  first block  \t\n\n\tsecond block\t"
        self.assertListEqual(markdown_to_blocks(markdown), ["first block", "second block"])

    def test_single_block_without_newlines_is_preserved(self):
        self.assertListEqual(markdown_to_blocks("single block"), ["single block"])

    def test_single_newlines_do_not_split_blocks(self):
        self.assertListEqual(markdown_to_blocks("first line\nsecond line"), ["first line\nsecond line"])

    def test_adjacent_content_is_split_at_block_separator(self):
        self.assertListEqual(markdown_to_blocks("first\n\nsecond"), ["first", "second"])
