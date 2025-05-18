class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props={}):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"{self.tag}, {self.value}, {self.children}, {self.props}"

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = ""
        for prop in self.props:
            result += f" {prop}=\"{self.props[prop]}\""
        return result

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props={}):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError("NO VALUE IN LEAF NODE")
        if self.tag == None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props={}):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag == None:
            raise ValueError("NO TAG IN PARENT NODE")
        if self.children == None:
            raise ValueError("NO CHILDREN IN PARENT NODE")
        result = ""
        for child in self.children:
            result += child.to_html()
        return f"<{self.tag}>{result}</{self.tag}>"
