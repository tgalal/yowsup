import unittest
from yowsup.structs import ProtocolTreeNode
from yowsup.layers.coder.encoder import WriteEncoder
from yowsup.layers.coder.tokendictionary import TokenDictionary

class EncoderTest(unittest.TestCase):
    def setUp(self):
        self.res = []
        self.encoder = WriteEncoder(TokenDictionary())

    def test_encode(self):
        node = ProtocolTreeNode("message", {"from": "abc", "to":"xyz"}, [ProtocolTreeNode("media", {"width" : "123"}, data=b"123456")])
        result = self.encoder.protocolTreeNodeToBytes(node)

        self.assertTrue(result in (
            [0, 248, 6, 9, 11, 252, 3, 120, 121, 122, 5, 252, 3, 97, 98, 99, 248, 1, 248, 4, 50, 238, 86, 255, 130, 18, 63,
             252, 6, 49, 50, 51, 52, 53, 54],
            [0, 248, 6, 9, 5, 252, 3, 97, 98, 99, 11, 252, 3, 120, 121, 122, 248, 1, 248, 4, 50, 238, 86, 255, 130, 18, 63,
             252, 6, 49, 50, 51, 52, 53, 54]
            )
        )

