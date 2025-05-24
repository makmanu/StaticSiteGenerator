from textnode import TextType
from textnode import TextNode
from htmlnode import LeafNode
from htmlnode import ParentNode
import re
from block import block_to_block_type
from block import BlockType

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
        
def text_to_children(text):
    children = []
    text_nodes = text_to_textnodes(text)
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def block_to_htmlnode(block_type, block):
    match block_type:
        case BlockType.PAR:
            return ParentNode("p", text_to_children(block.replace("\n", " ")))
        case BlockType.HEAD:
            count = 0
            while block[0] == "#":
                count += 1
                block = block[1:]
            block = block[1:]
            return ParentNode(f"h{count}", text_to_children(block.replace("\n", " ")))
        case BlockType.QUOTE:
            quote_list = block.split("\n")
            for i in range(len(quote_list)):
                quote_list[i] = quote_list[i][1:]
            quote = "\n".join(quote_list)
            return ParentNode("blockquote", text_to_children(quote.replace("\n", " ")))
        case BlockType.CODE:
            code = block.strip("`").lstrip("\n")
            return ParentNode("pre", [LeafNode("code", code),])
        case BlockType.UNLIST:
            list_of_items = block.split("\n")
            for i in range(len(list_of_items)):
                list_of_items[i] = "<li>" + list_of_items[i][2:] + "<li>"
            unlist = "\n".join(list_of_items)
            return ParentNode("ul", text_to_children(unlist.replace("\n", " ")))
        case BlockType.OLIST:
            list_of_items = block.split("\n")
            for i in range(len(list_of_items)):
                list_of_items[i] = "<li>" + list_of_items[i][3:] + "<li>"
            olist = "\n".join(list_of_items)
            return ParentNode("ol", text_to_children(olist.replace("\n", " ")))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        html_nodes.append(block_to_htmlnode(block_type, block))
    return ParentNode("div", html_nodes)


def main():
    md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
    print(markdown_to_html_node(md).to_html())

main()