from textnode import TextType
from textnode import TextNode
from htmlnode import LeafNode

def text_node_to_html_node(text_node):
    match text_node.text_type.value:
        case "TEXT":
            return LeafNode(None, text_node.text)
        case "BOLD":
            return LeafNode("b", text_node.text)
        case "ITALIC":
            return LeafNode("i", text_node.text)
        case "CODE":
            return LeafNode("code", text_node.text)
        case "LINK":
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case "IMG":
            return LeafNode("img", "", {"scr": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("UNKNOWN TEXTTYPE")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    for node in old_nodes:

def main():
    img_1 = TextNode("image text", TextType.IMG, "content/images/1.png")
    print(img_1)

main()