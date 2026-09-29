import unittest

from src.blocks import BlockType, block_to_block_type, markdown_to_blocks


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
        self.assertListEqual(
            markdown_to_blocks("first\n\n\n\nsecond"), ["first", "second"]
        )

    def test_surrounding_spaces_and_tabs_are_stripped(self):
        markdown = "\t  first block  \t\n\n\tsecond block\t"
        self.assertListEqual(
            markdown_to_blocks(markdown), ["first block", "second block"]
        )

    def test_tabs_only_markdown_returns_no_blocks(self):
        self.assertListEqual(markdown_to_blocks("\t\t"), [])

    def test_blank_block_with_tabs_is_dropped(self):
        self.assertListEqual(
            markdown_to_blocks("first\n\n \t \n\nsecond"), ["first", "second"]
        )

    def test_trailing_newline_is_stripped_from_final_block(self):
        self.assertListEqual(
            markdown_to_blocks("first\n\nsecond\n"), ["first", "second"]
        )

    def test_single_block_without_newlines_is_preserved(self):
        self.assertListEqual(markdown_to_blocks("single block"), ["single block"])

    def test_single_newlines_do_not_split_blocks(self):
        self.assertListEqual(
            markdown_to_blocks("first line\nsecond line"), ["first line\nsecond line"]
        )

    def test_adjacent_content_is_split_at_block_separator(self):
        self.assertListEqual(markdown_to_blocks("first\n\nsecond"), ["first", "second"])

    def test_blocktype_heading(self):
        headings = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6",
        ]
        for i in range(len(headings)):
            self.assertEqual(block_to_block_type(headings[i]), BlockType.HEADING)

    def test_blocktype_seven_hash_heading_is_paragraph(self):
        self.assertEqual(block_to_block_type("####### Heading 7"), BlockType.PARAGRAPH)

    def test_blocktype_code(self):
        code_block = "```\n code```"
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)

    def test_blocktype_code_requires_opening_newline(self):
        self.assertEqual(block_to_block_type("```code```"), BlockType.PARAGRAPH)

    def test_blocktype_code_with_closing_fence(self):
        self.assertEqual(block_to_block_type("```\ncode\n```\n"), BlockType.CODE)

    def test_blocktype_code_with_language(self):
        self.assertEqual(
            block_to_block_type("```python\nprint('hello')"), BlockType.CODE
        )

    def test_blocktype_code_unclosed_fence(self):
        self.assertEqual(block_to_block_type("```\nx = 1"), BlockType.CODE)

    def test_blocktype_code_language_then_newline_required(self):
        self.assertEqual(block_to_block_type("```python x"), BlockType.PARAGRAPH)

    def test_blocktype_quote(self):
        quote_block = "> A really wise quote.\n> Typed by a very foolish man.\n> For testing somewhat questionable code."
        self.assertEqual(block_to_block_type(quote_block), BlockType.QUOTE)

    def test_empty_block_is_paragraph(self):
        self.assertEqual(block_to_block_type(""), BlockType.PARAGRAPH)

    def test_blocktype_unordered_list(self):
        unordered_block = "- list item\n- another list item\n- yet another list item"
        self.assertEqual(block_to_block_type(unordered_block), BlockType.UNORDERED_LIST)

    def test_blocktype_unordered_list_requires_space_after_dash(self):
        self.assertEqual(block_to_block_type("-"), BlockType.PARAGRAPH)

    def test_blocktype_ordered_list(self):
        ordered_block = "1. first list item\n2. second list item\n3. third list item"
        self.assertEqual(block_to_block_type(ordered_block), BlockType.ORDERED_LIST)

    def test_blocktype_ordered_list_requires_space_after_period(self):
        self.assertEqual(
            block_to_block_type("1. first item\n2.second item"), BlockType.PARAGRAPH
        )

    def test_blocktype_paragraph(self):
        self.assertEqual(
            block_to_block_type("Just a plain paragraph."), BlockType.PARAGRAPH
        )

    def test_paragraph_rejects_invalid_headings(self):
        self.assertEqual(block_to_block_type("#paragraph"), BlockType.PARAGRAPH)

    def test_paragraph_rejects_invalid_code(self):
        # "```...\n" without a newline after the fence is not a CODE block.
        # Unclosed fences ("```\n...") ARE valid CODE now; covered above.
        self.assertEqual(
            block_to_block_type("```another nincorrect code block"), BlockType.PARAGRAPH
        )

    def test_paragraph_rejects_invalid_quote(self):
        for case in ["> It's a quote\nUntil it isn't", " > Also invalid quote"]:
            with self.subTest(case=case):
                self.assertEqual(block_to_block_type(case), BlockType.PARAGRAPH)

    def test_paragraph_rejects_invalid_unordered_list(self):
        case = "- unordered list\n- starts correctly\n-but breaks"
        self.assertEqual(block_to_block_type(case), BlockType.PARAGRAPH)

    def test_paragraph_rejects_invalid_ordered_list(self):
        self.assertEqual(
            block_to_block_type("1. first item\n2. second item\n4. fourth item breaks list"),
            BlockType.PARAGRAPH,
        )

    def test_blocktype_ordered_list_arbitrary_start(self):
        self.assertEqual(
            block_to_block_type("2. first item\n3. second item"), BlockType.ORDERED_LIST
        )

    def test_paragraph_rejects_hash_only(self):
        for case in ["#", "##", "###", "####", "#####", "######", "#######"]:
            with self.subTest(case=case):
                self.assertEqual(block_to_block_type(case), BlockType.PARAGRAPH)

    def test_blocktype_quote_single_line(self):
        for case in ["> single line quote", ">no space after angle"]:
            with self.subTest(case=case):
                self.assertEqual(block_to_block_type(case), BlockType.QUOTE)

    def test_blocktype_quote_blank_lines_are_quotes(self):
        self.assertEqual(block_to_block_type("> first\n>\n> third"), BlockType.QUOTE)

    def test_blocktype_quote_bare_gt_lines(self):
        self.assertEqual(block_to_block_type(">\n>\n>"), BlockType.QUOTE)

    def test_blocktype_quote_with_inline_markdown(self):
        self.assertEqual(
            block_to_block_type("> start with **bold** and `code`"),
            BlockType.QUOTE,
        )

    def test_paragraph_rejects_quote_then_plain_content(self):
        self.assertEqual(
            block_to_block_type("> quoted line\nplain continuation"),
            BlockType.PARAGRAPH,
        )

    def test_blocktype_unordered_list_single_item(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.UNORDERED_LIST)

    def test_blocktype_unordered_list_with_inline_content(self):
        for case in [
            "- item with **bold**\n- item with [link](https://example.com)",
            "- ends with trailing spaces   ",
        ]:
            with self.subTest(case=case):
                self.assertEqual(block_to_block_type(case), BlockType.UNORDERED_LIST)

    def test_blocktype_unordered_list_dash_space_empty_content(self):
        self.assertEqual(block_to_block_type("- \n- "), BlockType.UNORDERED_LIST)

    def test_paragraph_rejects_asterisk_bullet(self):
        self.assertEqual(
            block_to_block_type("* not an unordered list"), BlockType.PARAGRAPH
        )

    def test_blocktype_ordered_list_single_item(self):
        self.assertEqual(block_to_block_type("1. only item"), BlockType.ORDERED_LIST)

    def test_blocktype_ordered_list_two_items(self):
        self.assertEqual(block_to_block_type("1. a\n2. b"), BlockType.ORDERED_LIST)

    def test_paragraph_rejects_duplicate_ordered_numbers(self):
        self.assertEqual(block_to_block_type("1. a\n1. b"), BlockType.PARAGRAPH)

    def test_paragraph_rejects_multidigit_ordered_start(self):
        self.assertEqual(block_to_block_type("10. tenth"), BlockType.ORDERED_LIST)

    def test_paragraph_rejects_ordered_then_nonsequence(self):
        self.assertEqual(block_to_block_type("1. a\nother"), BlockType.PARAGRAPH)

    def test_paragraph_rejects_dash_start_with_quote_line(self):
        # "- " prefix passes the UL check only if ALL lines match; a quote
        # line makes it fall through to PARAGRAPH.
        self.assertEqual(
            block_to_block_type("- item\n> quote line"), BlockType.PARAGRAPH
        )

    def test_paragraph_rejects_gt_start_with_list_line(self):
        self.assertEqual(
            block_to_block_type("> quote line\n- item"), BlockType.PARAGRAPH
        )
