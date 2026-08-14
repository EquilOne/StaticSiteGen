from blocks import block_to_block_type, markdown_to_blocks
from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType


def main():
    text_node = TextNode("Test text", TextType.BOLD.value, "https://www.google.com")
    leaf_node = LeafNode("a", "link", {"href": "afakelink.com"})
    html_node = HTMLNode("p", "HTML node", [leaf_node])
    print(text_node.__repr__())
    print(leaf_node.__repr__())
    print(html_node.__repr__())


def markdown_to_html_node(markdown: str) -> HTMLNode:
    markdown_blocks = markdown_to_blocks(markdown)
    for block in markdown_blocks:
        block_type = block_to_block_type(block)


main()
