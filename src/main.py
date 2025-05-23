from textnode import TextType
from textnode import TextNode
from htmlnode import LeafNode
import re

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

def split_nodes_delimiter(old_nodes, delimiter):
    new_nodes = []
    match delimiter:
        case "**":
            new_text_type = TextType.BOLD
        case "_":
            new_text_type = TextType.ITALIC
        case "`":
            new_text_type = TextType.CODE
        case _:
            raise Exception("UNKNOWN DELIMITER")
    for node in old_nodes:
        if node.text_type.value != "TEXT":
            new_nodes.append(node)
        else:
            list_of_inlines = node.text.split(delimiter)
            for i in range(len(list_of_inlines)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(list_of_inlines[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(list_of_inlines[i], new_text_type))
    return new_nodes    

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        markdowns = extract_markdown_images(node.text)
        sections = [node.text]
        current_node_list = []
        if len(markdowns) != 0:
            for markdown in markdowns:
                new_sectinos = (sections[-1].split(f"![{markdown[0]}]({markdown[1]})"))
                del sections[-1]
                sections.extend(new_sectinos)
            for i in range(len(sections)):
                current_node_list.append(TextNode(sections[i],TextType.TEXT))
                if i != len(sections) - 1:
                    current_node_list.append(TextNode(markdowns[i][0], TextType.IMG, markdowns[i][1]))
        else:
            new_nodes.append(node)
    new_nodes.extend(current_node_list)
    return new_nodes
        
def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        markdowns = extract_markdown_links(node.text)
        sections = [node.text]
        current_node_list = []
        if len(markdowns) != 0:
            for markdown in markdowns:
                new_sectinos = (sections[-1].split(f"[{markdown[0]}]({markdown[1]})"))
                del sections[-1]
                sections.extend(new_sectinos)
            for i in range(len(sections)):
                current_node_list.append(TextNode(sections[i],TextType.TEXT))
                if i != len(sections) - 1:
                    current_node_list.append(TextNode(markdowns[i][0], TextType.LINK, markdowns[i][1]))
        else:
            new_nodes.append(node)
    new_nodes.extend(current_node_list)
    return new_nodes

def text_to_textnodes(text):
    node_prime = TextNode(text, TextType.TEXT)
    
def text_to_textnodes(text):
    original_node = [TextNode(text, TextType.TEXT),]
    new_nodes = split_nodes_delimiter(original_node, "**")
    new_nodes = split_nodes_delimiter(new_nodes, "_")
    new_nodes = split_nodes_delimiter(new_nodes, "`")
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    if new_nodes[-1].text == "":
        del new_nodes[-1]
    return new_nodes

def markdown_to_blocks(md):
    list_of_blocks = md.split("\n\n")
    striped = []
    result = []
    for block in list_of_blocks:
        striped.append(block.strip(" "))
    for i in range(len(striped)):
        if len(striped[i]) != 0:
            result.append(striped[i].strip("\n"))
    return result
        

def main():
    pass

main()