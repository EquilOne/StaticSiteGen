from enum import Enum

from src.constant import CODE_FENCE_RE, OL_NUM_RE
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
        if not no_hash.startswith(" "):
            return BlockType.PARAGRAPH
        if 1 <= count_leading_hashes(md_block) <= 6:
            return BlockType.HEADING
    if CODE_FENCE_RE.match(md_block):
        return BlockType.CODE
    if all(line.startswith(">") for line in md_block.splitlines()):
        return BlockType.QUOTE
    if all(line.startswith("- ") for line in md_block.splitlines()):
        return BlockType.UNORDERED_LIST
    if OL_NUM_RE.match(md_block):
        starting_index = int(OL_NUM_RE.match(md_block).group(1))
        block_lines = md_block.splitlines()
        for index, text in enumerate(block_lines):
            if not text.startswith(f"{starting_index}. "):
                return BlockType.PARAGRAPH
            else:
                starting_index += 1
                continue
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


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


def count_leading_hashes(md_block) -> int:
    i = 0
    count = 0
    while i < len(md_block) and md_block[i] == "#":
        count += 1
        i += 1
    return count
