import unittest

from src.htmlnode import LeafNode, ParentNode
from src.main import markdown_to_html_node


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
