import re

from src.blocks import (
    BlockType,
    block_to_block_type,
    count_leading_hashes,
    markdown_to_blocks,
)
from src.constant import CODE_FENCE_RE
from src.helpers import text_to_html_children
from src.htmlnode import HTMLNode, ParentNode
from src.textnode import TextNode, TextType, text_node_to_html_node


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
            match = CODE_FENCE_RE.match(block)
            if match:
                language = match.group(1)
                content = block.removeprefix(match.group(0))
                code_node = text_node_to_html_node(
                    TextNode(content.rstrip("`"), TextType.CODE)
                )
                if language:
                    code_node.props = {"class": "language-" + language}
                html_nodes.append(ParentNode("pre", [code_node]))
            else:
                code_node = text_node_to_html_node(TextNode(block, TextType.CODE))
                html_nodes.append(ParentNode("pre", [code_node]))
        if block_type == BlockType.QUOTE:
            lines = block.splitlines()
            line_nodes = []
            for line in lines:
                line = line.lstrip("> ").strip(" ")
                if line == "":
                    continue
                line_nodes.append(ParentNode("p", text_to_html_children(line)))
            html_nodes.append(ParentNode("blockquote", line_nodes))
        if (
            block_type == BlockType.ORDERED_LIST
            or block_type == BlockType.UNORDERED_LIST
        ):
            html_nodes.append(list_block_to_html_node(block))

    return ParentNode("div", html_nodes)


def list_block_to_html_node(md_block: str) -> HTMLNode:
    lines = md_block.splitlines()
    nodes = []
    if block_to_block_type(md_block) == BlockType.UNORDERED_LIST:
        for line in lines:
            clean_line = line.lstrip("- \t").strip(" ")
            content = text_to_html_children(clean_line)
            nodes.append(ParentNode("li", content))
        return ParentNode("ul", nodes)
    for line in lines:
        clean_line = line.lstrip("1234567890. \t").strip(" ")
        content = text_to_html_children(clean_line)
        nodes.append(ParentNode("li", content))
    return ParentNode("ol", nodes)
