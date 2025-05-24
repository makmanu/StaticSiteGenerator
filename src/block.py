from enum import Enum
import re

class BlockType(Enum):
    PAR = "paragraph"
    HEAD = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNLIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block):
    #Headings
    if len(re.findall(r"(?:^)#{1,6}\s", block)) != 0:
        return BlockType.HEAD
    #Code
    if len(re.findall(r"(?:^)\`\`\`([\s\S]*?)\`\`\`", block)) != 0:
        return BlockType.CODE
    
    block_lines = block.split("\n")

    #Quote
    check_quote = True
    for line in block_lines:
        if line[0] != ">":
            check_quote = False
    if check_quote:
        return BlockType.QUOTE
    
    #Unordered list
    check_unlist = True
    for line in block_lines:
        if line[0] != "-":
            check_unlist = False
    if check_unlist:
        return BlockType.UNLIST
    
    #Ordered list
    check_olist = True
    for i in range(len(block_lines)):
        if block_lines[i][0] != f"{i + 1}" or block_lines[i][1] != "." or block_lines[i][2] != " ":
            check_olist = False
    if check_olist:
        return BlockType.OLIST
    
    #Paragraph
    return BlockType.PAR