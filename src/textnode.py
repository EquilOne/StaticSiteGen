from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if not isinstance(other, TextNode):
            return NotImplemented
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode | None:
    if has_value(TextType, text_node.text_type):
        match text_node.text_type.value:
            case "text":
                return LeafNode(None, value=text_node.text)
            case "bold":
                return LeafNode("b", value=text_node.text)
            case "italic":
                return LeafNode("i", value=text_node.text)
            case "code":
                return LeafNode("code", value=text_node.text)
            case "link":
                if text_node.url is None:
                    raise ValueError("Invalid URL")
                return LeafNode("a", text_node.text, {"href": text_node.url})
            case "image":
                if text_node.url is None:
                    raise ValueError("Invalid URL")
                return LeafNode(
                    "img", "", {"src": text_node.url, "alt": text_node.text}
                )
    raise ValueError(f"Invalid text type: {text_node.text_type}")


def has_value(enum_type, value):
    try:
        enum_type(value)
        return True
    except ValueError:
        return False
