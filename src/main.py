from textnode import TextType
from textnode import TextNode

def main():
    img_1 = TextNode("image text", TextType.IMG, "content/images/1.png")
    print(img_1)

main()