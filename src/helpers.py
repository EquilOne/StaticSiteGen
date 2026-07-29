import re

from src.textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        old_node_splits = old_node.text.split(delimiter)
        if len(old_node_splits) % 2 == 0:
            raise ValueError(
                "Invalid markdown syntax: no matching formatting delimiter"
            )
        for i in range(len(old_node_splits)):
            if not old_node_splits[i]:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(old_node_splits[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(old_node_splits[i], text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text: str) -> list[tuple]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
