from textnode import TextNode, TextType


def main():
    print(TextType.BOLD, TextType.BOLD.value)
    node = TextNode("Test text", TextType.BOLD.value, "https://www.google.com")
    print(node.__repr__())


main()
