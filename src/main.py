import re

from src.blocks import (
    BlockType,
    block_to_block_type,
    count_leading_hashes,
    markdown_to_blocks,
)
from src.helpers import text_to_html_children
from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.textnode import TextNode, TextType, text_node_to_html_node


def main():
    text_node = TextNode("Test text", TextType.BOLD, "https://www.google.com")
    leaf_node = LeafNode("a", "link", {"href": "afakelink.com"})
    html_node = HTMLNode("p", "HTML node", [leaf_node])
    print(text_node.__repr__())
    print(leaf_node.__repr__())
    print(html_node.__repr__())


def markdown_to_html_node(markdown: str) -> HTMLNode:
    markdown_blocks: list[str] = markdown_to_blocks(markdown)
    html_nodes = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            html_nodes.append(ParentNode("p", text_to_html_children(block)))
        if block_type == BlockType.HEADING:
            heading_level = count_leading_hashes(block)
            if heading_level not in range(1, 7):
                raise ValueError(f"Invalid heading level: {heading_level}")
            content = re.sub(r"[ \t]+#+[ \t]*$", "", block.lstrip("#").strip())
            html_nodes.append(
                ParentNode(f"h{heading_level}", text_to_html_children(content))
            )
        if block_type == BlockType.CODE:
            code_node: list[HTMLNode] = [
                text_node_to_html_node(TextNode(block, TextType.CODE))
            ]
            html_nodes.append(ParentNode("pre", code_node))

    return ParentNode("div", html_nodes)


main()
