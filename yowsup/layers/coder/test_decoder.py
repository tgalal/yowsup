import unittest
from yowsup.layers.coder.decoder import ReadDecoder
from yowsup.layers.coder.tokendictionary import TokenDictionary
from yowsup.structs import ProtocolTreeNode
class DecoderTest(unittest.TestCase):
    def setUp(self):
        self.decoder = ReadDecoder(TokenDictionary())
        self.decoder.streamStarted = True

    def test_decode(self):
        data = bytearray([0, 248, 6, 9, 11, 252, 3, 120, 121, 122, 5, 252, 3, 97, 98, 99, 248, 1, 248, 4, 50, 238, 86, 255, 130, 18, 63,
             252, 6, 49, 50, 51, 52, 53, 54])
        node = self.decoder.getProtocolTreeNode(data)
        targetNode = ProtocolTreeNode("message", {"from": "abc", "to":"xyz"}, [ProtocolTreeNode("media", {"width" : "123"}, data=b"123456")])
        self.assertEqual(node, targetNode)
