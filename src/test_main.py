import unittest

from textnode import TextType
from textnode import TextNode
from htmlnode import LeafNode
from main import text_node_to_html_node

class TestMain(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node_img = TextNode("description of img", TextType.IMG, "notfake.com/img1")
        html_node = text_node_to_html_node(node)
        html_node_img = text_node_to_html_node(node_img)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node_img.value, "")
        self.assertEqual(html_node_img.tag, "img")