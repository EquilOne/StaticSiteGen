import re

from src.textnode import TextNode, TextType


def text_to_textnodes(text: str) -> list[TextNode]:
    delimiters = {TextType.BOLD: "**", TextType.ITALIC: "_", TextType.CODE: "`"}
    new_nodes = [TextNode(text, TextType.TEXT)]
    for k, v in delimiters.items():
        new_nodes = split_nodes_delimiter(new_nodes, v, k)
    new_nodes = split_nodes_image_and_link(new_nodes)
    return new_nodes


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


def split_nodes_image_and_link(old_nodes: list[TextNode]) -> list[TextNode]:
    final_nodes: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            final_nodes.append(old_node)
            continue
        images: list[tuple[str, str]] = extract_markdown_images(old_node.text)
        links: list[tuple[str, str]] = extract_markdown_links(old_node.text)
        if not old_node.text:
            continue
        if not links and not images:
            final_nodes.append(old_node)
            continue
        if not images:
            final_nodes.extend(split_nodes_link(old_node, links))
            continue
        final_nodes.extend(
            split_nodes_image_and_link(split_nodes_image(old_node, images))
        )
    return final_nodes


def split_nodes_image(
    old_node: TextNode, images: list[tuple[str, str]] | None = None
) -> list[TextNode]:
    if old_node.text_type != TextType.TEXT:
        return [old_node]
    new_nodes = []
    original_text = old_node.text
    sections = []
    if images is None:
        images = extract_markdown_images(old_node.text)
    for i in range(len(images)):
        sections: list[str] = original_text.split(
            f"![{images[i][0]}]({images[i][1]})", maxsplit=1
        )
        original_text: str = sections[1]
        if sections[0] == "":
            new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
            continue
        new_nodes.append(TextNode(sections[0], TextType.TEXT))
        new_nodes.append(TextNode(images[i][0], TextType.IMAGE, images[i][1]))
    if original_text != "":
        new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(
    old_node: TextNode, links: list[tuple[str, str]] | None = None
) -> list[TextNode]:
    if old_node.text_type != TextType.TEXT:
        return [old_node]
    new_nodes = []
    original_text: str = old_node.text
    sections = []
    if links is None:
        links = extract_markdown_links(old_node.text)
    for i in range(len(links)):
        sections: list[str] = original_text.split(
            f"[{links[i][0]}]({links[i][1]})", maxsplit=1
        )
        original_text = sections[1]
        if sections[0] == "":
            new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
            continue
        new_nodes.append(TextNode(sections[0], TextType.TEXT))
        new_nodes.append(TextNode(links[i][0], TextType.LINK, links[i][1]))
    if original_text != "":
        new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches
