import unittest
from yowsup.structs import ProtocolTreeNode
from yowsup.layers.coder.encoder import WriteEncoder
from yowsup.layers.coder.tokendictionary import TokenDictionary

class EncoderTest(unittest.TestCase):
    def setUp(self):
        self.res = []
        self.encoder = WriteEncoder(TokenDictionary())

    def test_encode(self):
        node = ProtocolTreeNode("message", {"form": "abc", "to":"xyz"}, [ProtocolTreeNode("media", {"width" : "123"}, data="123456")])
        result = self.encoder.protocolTreeNodeToBytes(node)

        self.assertTrue(result in (
            [248, 6, 95, 179, 252, 3, 120, 121, 122, 252, 4, 102, 111, 114, 109, 252, 3, 97, 98, 99, 248, 1, 248, 4, 93,
             236, 104, 255, 130, 18, 63, 252, 6, 49, 50, 51, 52, 53, 54],
            [248, 6, 95, 252, 4, 102, 111, 114, 109, 252, 3, 97, 98, 99, 179, 252, 3, 120, 121, 122, 248, 1, 248, 4, 93,
             236, 104, 255, 130, 18, 63, 252, 6, 49, 50, 51, 52, 53, 54]
            )
        )

