import unittest

from src.htmlnode import LeafNode, ParentNode
from src.convert import markdown_to_html_node


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraph(self):
        block = "This is a basic test paragraph."
        html_node = markdown_to_html_node(block)
        expected_html_node = ParentNode(
            "div",
            [ParentNode("p", [LeafNode(None, "This is a basic test paragraph.")])],
        )
        self.assertEqual(html_node, expected_html_node)

    def test_heading_h1(self):
        html_node = markdown_to_html_node("# Hello")
        expected = ParentNode("div", [ParentNode("h1", [LeafNode(None, "Hello")])])
        self.assertEqual(html_node, expected)

    def test_heading_h6(self):
        html_node = markdown_to_html_node("###### Six")
        expected = ParentNode("div", [ParentNode("h6", [LeafNode(None, "Six")])])
        self.assertEqual(html_node, expected)

    def test_heading_inline_formatting(self):
        html_node = markdown_to_html_node("# Title with **bold**")
        expected = ParentNode(
            "div",
            [
                ParentNode(
                    "h1",
                    [LeafNode(None, "Title with "), LeafNode("b", "bold")],
                )
            ],
        )
        self.assertEqual(html_node, expected)

    def test_heading_multiple_spaces(self):
        html_node = markdown_to_html_node("#  Two spaces")
        expected = ParentNode("div", [ParentNode("h1", [LeafNode(None, "Two spaces")])])
        self.assertEqual(html_node, expected)

    def test_heading_closing_sequence(self):
        html_node = markdown_to_html_node("## Title ##")
        expected = ParentNode("div", [ParentNode("h2", [LeafNode(None, "Title")])])
        self.assertEqual(html_node, expected)

    def test_heading_keeps_glued_hash(self):
        html_node = markdown_to_html_node("# C#")
        expected = ParentNode("div", [ParentNode("h1", [LeafNode(None, "C#")])])
        self.assertEqual(html_node, expected)

    def test_heading_interior_hashes(self):
        html_node = markdown_to_html_node("# ## x")
        expected = ParentNode("div", [ParentNode("h1", [LeafNode(None, "## x")])])
        self.assertEqual(html_node, expected)

    def test_hashtag_is_paragraph(self):
        html_node = markdown_to_html_node("#hashtag")
        expected = ParentNode("div", [ParentNode("p", [LeafNode(None, "#hashtag")])])
        self.assertEqual(html_node, expected)

    def test_seven_hashes_is_paragraph(self):
        html_node = markdown_to_html_node("####### x")
        expected = ParentNode("div", [ParentNode("p", [LeafNode(None, "####### x")])])
        self.assertEqual(html_node, expected)

    def test_paragraph_and_heading_mixed(self):
        html_node = markdown_to_html_node("Some text.\n\n# Header")
        expected = ParentNode(
            "div",
            [
                ParentNode("p", [LeafNode(None, "Some text.")]),
                ParentNode("h1", [LeafNode(None, "Header")]),
            ],
        )
        self.assertEqual(html_node, expected)

    def test_code_block_simple(self):
        html_node = markdown_to_html_node("```\ncode here\n```")
        expected = ParentNode(
            "div",
            [
                ParentNode(
                    "pre",
                    [LeafNode("code", "code here\n")],
                )
            ],
        )
        self.assertEqual(html_node, expected)

    def test_code_block_multiline(self):
        html_node = markdown_to_html_node("```\nline one\nline two\nline three\n```")
        expected = ParentNode(
            "div",
            [
                ParentNode(
                    "pre",
                    [LeafNode("code", "line one\nline two\nline three\n")],
                )
            ],
        )
        self.assertEqual(html_node, expected)

    def test_code_block_with_paragraph(self):
        html_node = markdown_to_html_node("Before.\n\n```\nx = 1\n```\n\nAfter.")
        expected = ParentNode(
            "div",
            [
                ParentNode("p", [LeafNode(None, "Before.")]),
                ParentNode("pre", [LeafNode("code", "x = 1\n")]),
                ParentNode("p", [LeafNode(None, "After.")]),
            ],
        )
        self.assertEqual(html_node, expected)

    def test_code_block_empty_content(self):
        html_node = markdown_to_html_node("```\n```")
        expected = ParentNode(
            "div",
            [ParentNode("pre", [LeafNode("code", "")])],
        )
        self.assertEqual(html_node, expected)

    def test_code_block_fence_prefix_stripped(self):
        html_node = markdown_to_html_node("```js\nconst x = 1;\nconst y = 2;")
        expected = ParentNode(
            "div",
            [
                ParentNode(
                    "pre",
                    [
                        LeafNode(
                            "code",
                            "const x = 1;\nconst y = 2;",
                            {"class": "language-js"},
                        )
                    ],
                )
            ],
        )
        self.assertEqual(html_node, expected)

    def test_code_block_language_prop(self):
        html_node = markdown_to_html_node("```python\nprint('hello')\n```")
        expected = ParentNode(
            "div",
            [
                ParentNode(
                    "pre",
                    [
                        LeafNode(
                            "code",
                            "print('hello')\n",
                            {"class": "language-python"},
                        )
                    ],
                )
            ],
        )
        self.assertEqual(html_node, expected)

    def test_code_block_bare_fence_no_props(self):
        html_node = markdown_to_html_node("```\nbare\n```")
        expected = ParentNode(
            "div",
            [ParentNode("pre", [LeafNode("code", "bare\n", None)])],
        )
        self.assertEqual(html_node, expected)

    def test_code_block_unclosed_fence(self):
        html_node = markdown_to_html_node("```\nnever closed")
        expected = ParentNode(
            "div",
            [ParentNode("pre", [LeafNode("code", "never closed")])],
        )
        self.assertEqual(html_node, expected)

    def test_inline_code_span_untouched(self):
        html_node = markdown_to_html_node("Value ```x = 1``` here.")
        expected = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode(None, "Value "),
                        LeafNode("code", "x = 1"),
                        LeafNode(None, " here."),
                    ],
                )
            ],
        )
        self.assertEqual(html_node, expected)
