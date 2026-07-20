from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType


def main():
    text_node = TextNode("Test text", TextType.BOLD.value, "https://www.google.com")
    leaf_node = LeafNode("a", "link", {"href": "afakelink.com"})
    html_node = HTMLNode("p", "HTML node", [leaf_node])
    print(text_node.__repr__())
    print(leaf_node.__repr__())
    print(html_node.__repr__())


main()
