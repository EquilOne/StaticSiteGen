import unittest

from src.helpers import extract_markdown_images, extract_markdown_links, split_nodes_delimiter
from src.textnode import TextNode, TextType


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

    def test_empty_node_list(self):
        result = split_nodes_delimiter([], "**", TextType.BOLD)
        self.assertListEqual([], result)

    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual([], result)

    def test_consecutive_delimiters(self):
        node = TextNode("a **b****c** d", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.BOLD),
            TextNode("c", TextType.BOLD),
            TextNode(" d", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_italic_delimiter(self):
        node = TextNode("This is *italic* text.", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_code_delimiter(self):
        node = TextNode("This is `code` here.", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_mixed_node_types_input(self):
        node1 = TextNode("plain text", TextType.TEXT)
        node2 = TextNode("already bold", TextType.BOLD)
        node3 = TextNode("also plain", TextType.TEXT)
        result = split_nodes_delimiter([node1, node2, node3], "**", TextType.BOLD)
        expected = [TextNode("plain text", TextType.TEXT), node2, TextNode("also plain", TextType.TEXT)]
        self.assertEqual(result, expected)


class TestExtractors(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/abc123.png)"
        )
        self.assertListEqual(
            [("image", "https://i.imgur.com/zjjcJKZ.png"), ("another", "https://i.imgur.com/abc123.png")],
            matches,
        )

    def test_extract_markdown_images_none(self):
        matches = extract_markdown_images("This is text with no images.")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_string(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_no_alt(self):
        matches = extract_markdown_images("![](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
            matches,
        )

    def test_extract_markdown_links_none(self):
        matches = extract_markdown_links("This is text with no links.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_empty_string(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_no_text(self):
        matches = extract_markdown_links("[](https://www.boot.dev)")
        self.assertListEqual([("", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_excludes_images(self):
        matches = extract_markdown_links(
            "This has an ![image](https://img.com/1.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual([("link", "https://boot.dev")], matches)

    def test_extract_markdown_images_and_links_mixed(self):
        text = "![img](https://img.com/a.png) and [link](https://boot.dev)"
        img_matches = extract_markdown_images(text)
        link_matches = extract_markdown_links(text)
        self.assertListEqual([("img", "https://img.com/a.png")], img_matches)
        self.assertListEqual([("link", "https://boot.dev")], link_matches)
