import unittest

from splitnodes import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNodes(unittest.TestCase):
    def setUp(self):
        self.nodes = [
            TextNode("What a **bold** choice.", TextType.TEXT),
            TextNode("**Bold** way to start a sentence.", TextType.TEXT),
            TextNode("This text ends in **bold**.", TextType.TEXT),
            TextNode("**This** is how to _emphasize_ text, **boldly**.", TextType.TEXT),
            TextNode("This is plain text.", TextType.TEXT),
        ]

    def test_single_bold_node(self):
        result = split_nodes_delimiter(self.nodes[:1], "**", TextType.BOLD)
        expected = [
            TextNode("What a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" choice.", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_start_bold_node(self):
        result = split_nodes_delimiter(self.nodes[1:2], "**", TextType.BOLD)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" way to start a sentence.", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_end_bold_node(self):
        result = split_nodes_delimiter(self.nodes[2:3], "**", TextType.BOLD)
        expected = [
            TextNode("This text ends in ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(".", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_multiple_different_nodes(self):
        result = split_nodes_delimiter(self.nodes[3:4], "**", TextType.BOLD)
        expected = [
            TextNode("This", TextType.BOLD),
            TextNode(" is how to _emphasize_ text, ", TextType.TEXT),
            TextNode("boldly", TextType.BOLD),
            TextNode(".", TextType.TEXT),
        ]

        self.assertEqual(result, expected)

    def test_plain_node(self):
        result = split_nodes_delimiter(self.nodes[4:], "**", TextType.BOLD)
        expected = [TextNode("This is plain text.", TextType.TEXT)]

        self.assertEqual(result, expected)

    def test_unmatched_delimiter_raises(self):
        node = TextNode("unclosed **bold here.", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_nontext_node_passes(self):
        node = TextNode("I am bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [node]

        self.assertEqual(result, expected)
