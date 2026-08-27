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
