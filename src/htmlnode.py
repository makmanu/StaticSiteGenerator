class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
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