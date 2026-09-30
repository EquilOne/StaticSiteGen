import os
import shutil

from src.convert import markdown_to_html_node
from src.htmlnode import HTMLNode, LeafNode
from src.textnode import TextNode, TextType


def copy_files(src_dir: str, dst_dir: str):
    cwd_path = os.getcwd()
    dst_dir_path = os.path.join(dst_dir, cwd_path)
    if os.path.exists(dst_dir_path):
        shutil.rmtree(dst_dir_path)


def main():
    text_node = TextNode("Test text", TextType.BOLD, "https://www.google.com")
    leaf_node = LeafNode("a", "link", {"href": "afakelink.com"})
    html_node = HTMLNode("p", "HTML node", [leaf_node])
    html_code_node = markdown_to_html_node(
        "```\nPretend this is actually a code block.```"
    )
    print(text_node.__repr__())
    print(leaf_node.__repr__())
    print(html_node.__repr__())
    print(html_code_node.__repr__())


main()
