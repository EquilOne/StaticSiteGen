import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        multiple_props = HTMLNode(props={"id": "paragraph", "onClick": "handleClick"})
        empty_dict = HTMLNode(props={})
        is_none = HTMLNode(props=None)

        self.assertEqual(
            multiple_props.props_to_html(), ' id="paragraph" onClick="handleClick"'
        )
        self.assertEqual(empty_dict.props_to_html(), "")
        self.assertEqual(is_none.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "link", {"href": "www.smoogle.com"})
        self.assertEqual(node.to_html(), '<a href="www.smoogle.com">link</a>')


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("p", "Follow the link below, to my super awesome blog!")
        child_node_link = LeafNode("a", "link", {"href": "totallylegitwebsite.com"})
        parent_node = ParentNode("div", [child_node, child_node_link], {"id": "parent"})
        self.assertEqual(
            parent_node.to_html(),
            '<div id="parent"><p>Follow the link below, to my super awesome blog!</p><a href="totallylegitwebsite.com">link</a></div>',
        )
