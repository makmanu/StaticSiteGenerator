import unittest

from textnode import TextType
from textnode import TextNode
from htmlnode import LeafNode
from main import text_node_to_html_node
from main import split_nodes_delimiter
from main import extract_markdown_images

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
    
    def test_split_nodes_delimiter(self):
        node = TextNode("plain text", TextType.TEXT)
        node2 = TextNode("**bold** text", TextType.TEXT)
        node3 = TextNode("really _italic_ text", TextType.TEXT)
        node4 = TextNode("a `code one` and `code two` text", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node, node2], "**"), [TextNode("plain text", TextType.TEXT, None), TextNode("", TextType.TEXT, None), TextNode("bold", TextType.BOLD, None), TextNode(" text", TextType.TEXT, None)])
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        print(matches)