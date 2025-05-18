import unittest

from htmlnode import HTMLNode
from htmlnode import LeafNode
from htmlnode import ParentNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "this is test", None, {"kek": "ladno", "mom": None})
        node2 = HTMLNode("p", "this is ball", None, {"kek": "ladno", "mom": None})
        node3 = HTMLNode("a", "this is test", None, {"kek": "ladno", "mom": "One"})
        node4 = HTMLNode("a", "this is test", None, {"kek": "ladno", "mom": None})
        self.assertEqual(node.props_to_html(), node2.props_to_html())
        self.assertEqual(node.props_to_html(), node4.props_to_html())
        self.assertNotEqual(node.props_to_html(), node3.props_to_html())

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        node2 = LeafNode("a", "Hello, world!", {"href": "content/images/1.png"})
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        self.assertEqual(node2.to_html(), "<a href=\"content/images/1.png\">Hello, world!</a>")
    
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

if __name__ == "__main__":
    unittest.main()