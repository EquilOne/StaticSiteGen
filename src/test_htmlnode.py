import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        multiple_props = HTMLNode(props={"id": "paragraph", "onClick": "handleClick"})
        empty_dict = HTMLNode(props={})
        is_none = HTMLNode(props=None)
        missing_props = HTMLNode(tag="p", value="This is a paragraph")

        self.assertEqual(
            multiple_props.props_to_html(), ' id="paragraph" onClick="handleClick"'
        )
        self.assertEqual(empty_dict.props_to_html(), "")
        self.assertEqual(is_none.props_to_html(), "")
        self.assertEqual(missing_props.props_to_html(), "")
