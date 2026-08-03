import unittest

from src.helpers import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_image_and_link,
    split_nodes_link,
    text_to_textnodes,
)
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
        expected = [
            TextNode("plain text", TextType.TEXT),
            node2,
            TextNode("also plain", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image(node)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_no_image(self):
        node = TextNode("This is text with no images.", TextType.TEXT)
        new_nodes = split_nodes_image(node)
        self.assertListEqual([node], new_nodes)

    def test_split_images_leading(self):
        node = TextNode(
            "![leading image](https://thisisnotarealimage.png) This string begins with an image.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image(node)
        self.assertListEqual(
            [
                TextNode(
                    "leading image", TextType.IMAGE, "https://thisisnotarealimage.png"
                ),
                TextNode(" This string begins with an image.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_trailing(self):
        node = TextNode(
            "This string ends with an image. ![trailing image](https://thisisnotarealimage.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image(node)
        self.assertListEqual(
            [
                TextNode("This string ends with an image. ", TextType.TEXT),
                TextNode(
                    "trailing image", TextType.IMAGE, "https://thisisnotarealimage.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link(node)
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_images_empty(self):
        node = TextNode("", TextType.TEXT)
        self.assertListEqual([], split_nodes_image(node))

    def test_split_images_consecutive(self):
        node = TextNode("![a](u)![b](v)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "u"),
                TextNode("b", TextType.IMAGE, "v"),
            ],
            split_nodes_image(node),
        )

    def test_split_images_image_only(self):
        node = TextNode("![a](u)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("a", TextType.IMAGE, "u")],
            split_nodes_image(node),
        )

    def test_split_images_nontext(self):
        node = TextNode("bold", TextType.BOLD)
        self.assertListEqual([TextNode("bold", TextType.BOLD)], split_nodes_image(node))

    def test_split_images_empty_alt(self):
        node = TextNode("![](u) text", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("", TextType.IMAGE, "u"),
                TextNode(" text", TextType.TEXT),
            ],
            split_nodes_image(node),
        )

    def test_split_images_explicit(self):
        node = TextNode("![img](u)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("img", TextType.IMAGE, "u")],
            split_nodes_image(node, [("img", "u")]),
        )

    def test_split_links_empty(self):
        node = TextNode("", TextType.TEXT)
        self.assertListEqual([], split_nodes_link(node))

    def test_split_links_no_links(self):
        node = TextNode("no links", TextType.TEXT)
        self.assertListEqual(
            [TextNode("no links", TextType.TEXT)],
            split_nodes_link(node),
        )

    def test_split_links_leading(self):
        node = TextNode("[link](u) text", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "u"),
                TextNode(" text", TextType.TEXT),
            ],
            split_nodes_link(node),
        )

    def test_split_links_trailing(self):
        node = TextNode("text [link](u)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("text ", TextType.TEXT),
                TextNode("link", TextType.LINK, "u"),
            ],
            split_nodes_link(node),
        )

    def test_split_links_consecutive(self):
        node = TextNode("[a](u)[b](v)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("a", TextType.LINK, "u"),
                TextNode("b", TextType.LINK, "v"),
            ],
            split_nodes_link(node),
        )

    def test_split_links_link_only(self):
        node = TextNode("[a](u)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("a", TextType.LINK, "u")],
            split_nodes_link(node),
        )

    def test_split_links_nontext(self):
        node = TextNode("bold", TextType.BOLD)
        self.assertListEqual([TextNode("bold", TextType.BOLD)], split_nodes_link(node))

    def test_split_links_empty_text(self):
        node = TextNode("[](u)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("", TextType.LINK, "u")],
            split_nodes_link(node),
        )

    def test_split_links_explicit(self):
        node = TextNode("[link](u)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("link", TextType.LINK, "u")],
            split_nodes_link(node, [("link", "u")]),
        )


class TestOrchestrator(unittest.TestCase):
    def test_plain_text(self):
        result = split_nodes_image_and_link([TextNode("Just text.", TextType.TEXT)])
        self.assertListEqual(
            [TextNode("Just text.", TextType.TEXT)],
            result,
        )

    def test_nontext_node_passes(self):
        result = split_nodes_image_and_link([TextNode("**bold**", TextType.BOLD)])
        self.assertListEqual(
            [TextNode("**bold**", TextType.BOLD)],
            result,
        )

    def test_empty_list(self):
        result = split_nodes_image_and_link([])
        self.assertListEqual([], result)

    def test_empty_text(self):
        result = split_nodes_image_and_link([TextNode("", TextType.TEXT)])
        self.assertListEqual([], result)

    def test_image_only(self):
        result = split_nodes_image_and_link(
            [TextNode("![alt](img.png)", TextType.TEXT)]
        )
        self.assertListEqual(
            [TextNode("alt", TextType.IMAGE, "img.png")],
            result,
        )

    def test_link_only(self):
        result = split_nodes_image_and_link(
            [TextNode("[text](url.com)", TextType.TEXT)]
        )
        self.assertListEqual(
            [TextNode("text", TextType.LINK, "url.com")],
            result,
        )

    def test_image_then_link(self):
        result = split_nodes_image_and_link(
            [TextNode("![img](u) and [link](v)", TextType.TEXT)]
        )
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "u"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "v"),
            ],
            result,
        )

    def test_multiple_images_and_links(self):
        result = split_nodes_image_and_link(
            [
                TextNode(
                    "![a](1) text [b](2) more ![c](3) end",
                    TextType.TEXT,
                )
            ]
        )
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "1"),
                TextNode(" text ", TextType.TEXT),
                TextNode("b", TextType.LINK, "2"),
                TextNode(" more ", TextType.TEXT),
                TextNode("c", TextType.IMAGE, "3"),
                TextNode(" end", TextType.TEXT),
            ],
            result,
        )

    def test_collision_regression(self):
        result = split_nodes_image_and_link(
            [TextNode("![same](u) and [same](u)", TextType.TEXT)]
        )
        self.assertListEqual(
            [
                TextNode("same", TextType.IMAGE, "u"),
                TextNode(" and ", TextType.TEXT),
                TextNode("same", TextType.LINK, "u"),
            ],
            result,
        )

    def test_multiple_input_nodes(self):
        result = split_nodes_image_and_link(
            [
                TextNode("![img](u)", TextType.TEXT),
                TextNode("[link](v)", TextType.TEXT),
            ]
        )
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "u"),
                TextNode("link", TextType.LINK, "v"),
            ],
            result,
        )


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
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("another", "https://i.imgur.com/abc123.png"),
            ],
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
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
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

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        matches = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(matches, text_to_textnodes(text))


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text_only(self):
        self.assertListEqual(
            [TextNode("plain text", TextType.TEXT)],
            text_to_textnodes("plain text"),
        )

    def test_only_bold_text(self):
        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            text_to_textnodes("**bold**"),
        )

    def test_only_italic_text(self):
        self.assertListEqual(
            [TextNode("italic", TextType.ITALIC)],
            text_to_textnodes("_italic_"),
        )

    def test_only_code(self):
        self.assertListEqual(
            [TextNode("code", TextType.CODE)],
            text_to_textnodes("`code`"),
        )

    def test_only_image(self):
        self.assertListEqual(
            [TextNode("alt", TextType.IMAGE, "url")],
            text_to_textnodes("![alt](url)"),
        )

    def test_only_link(self):
        self.assertListEqual(
            [TextNode("text", TextType.LINK, "url")],
            text_to_textnodes("[text](url)"),
        )

    def test_empty_string(self):
        self.assertListEqual([], text_to_textnodes(""))

    def test_formatted_element_at_start(self):
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" at start", TextType.TEXT),
            ],
            text_to_textnodes("**bold** at start"),
        )

    def test_formatted_element_at_end(self):
        self.assertListEqual(
            [
                TextNode("end with ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            text_to_textnodes("end with _italic_"),
        )

    def test_consecutive_formatting(self):
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
            ],
            text_to_textnodes("**bold**_italic_"),
        )

    def test_unmatched_delimiter_raises_value_error(self):
        with self.assertRaises(ValueError):
            text_to_textnodes("this is **unclosed")

    def test_images_and_links_without_delimiter_formatting(self):
        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "url"),
                TextNode(" and ", TextType.TEXT),
                TextNode("text", TextType.LINK, "url2"),
            ],
            text_to_textnodes("![alt](url) and [text](url2)"),
        )

    def test_mixed_bold_and_italic_only(self):
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            text_to_textnodes("**bold** and _italic_"),
        )
