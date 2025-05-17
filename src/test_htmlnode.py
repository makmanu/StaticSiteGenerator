import unittest

from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "this is test", None, {"kek": "ladno", "mom": None})
        node2 = HTMLNode("p", "this is ball", None, {"kek": "ladno", "mom": None})
        node3 = HTMLNode("a", "this is test", None, {"kek": "ladno", "mom": "One"})
        node4 = HTMLNode("a", "this is test", None, {"kek": "ladno", "mom": None})
        self.assertEqual(node.props_to_html(), node2.props_to_html())
        self.assertEqual(node.props_to_html(), node4.props_to_html())
        self.assertNotEqual(node.props_to_html(), node3.props_to_html())

if __name__ == "__main__":
    unittest.main()