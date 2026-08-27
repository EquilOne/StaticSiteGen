from enum import Enum

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    raw_blocks = markdown.split("\n\n")
    blocks = []
    for raw_block in raw_blocks:
        raw_block = raw_block.strip()
        if not raw_block:
            continue
        blocks.append(raw_block.strip())
    return blocks


def block_to_block_type(md_block: str) -> BlockType:
    if md_block == "":
        return BlockType.PARAGRAPH
    if md_block.startswith("#"):
        no_hash = md_block.lstrip("#")
        hash_count = len(md_block) - len(no_hash)
        if not no_hash.startswith(" "):
            return BlockType.PARAGRAPH
        if 1 <= hash_count <= 6:
            return BlockType.HEADING
    if md_block.startswith("```\n") and md_block.endswith("```"):
        return BlockType.CODE
    if all(line.startswith(">") for line in md_block.splitlines()):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in md_block.splitlines()):
        return BlockType.UNORDERED_LIST
    if md_block.startswith("1. "):
        block_lines = md_block.splitlines()
        for index, text in enumerate(block_lines):
            if not text.startswith(f"{index + 1}. "):
                return BlockType.PARAGRAPH
            else:
                continue
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def heading_to_heading_level(block: str) -> int:
    if block_to_block_type(block) == BlockType.HEADING and type(block[1]) == "int":
        return int(block[1])
    return 0


def list_block_to_html_node(md_block: str) -> HTMLNode:
    lines = md_block.splitlines()
    nodes = []
    if block_to_block_type(md_block) == BlockType.UNORDERED_LIST:
        for line in lines:
            nodes.append(LeafNode("li", line.strip("- \t")))
        return ParentNode("ul", nodes)
    for line in lines:
        nodes.append(LeafNode("li", line.strip("1234567890. \t")))
    return ParentNode("ol", nodes)
