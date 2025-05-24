import unittest

from block import BlockType
from block import block_to_block_type
from main import markdown_to_blocks

class TestBlock(unittest.TestCase):
    def test_block_to_block_type(self):
        Head = "### This is heading"
        Code = """```
This is code
```
"""
        Quote = ">This is quote"

        self.assertEqual(block_to_block_type(Head), BlockType.HEAD)
        self.assertEqual(block_to_block_type(Code), BlockType.CODE)
        self.assertEqual(block_to_block_type(Quote), BlockType.QUOTE)