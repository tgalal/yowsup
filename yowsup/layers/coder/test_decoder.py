import unittest
from yowsup.layers.coder.decoder import ReadDecoder
from yowsup.layers.coder.tokendictionary import TokenDictionary
from yowsup.structs import ProtocolTreeNode
class DecoderTest(unittest.TestCase):
    def setUp(self):
        self.decoder = ReadDecoder(TokenDictionary())
        self.decoder.streamStarted = True

    def test_decode(self):
        data = [248, 6, 89, 165, 252, 3, 120, 121, 122, 252, 4, 102, 111, 114, 109, 252, 3, 97, 98, 99, 248, 1,
                                  248, 4, 87, 236, 99, 252, 3, 49, 50, 51, 252, 6, 49, 50, 51, 52, 53, 54]
        node = self.decoder.getProtocolTreeNode(data)
        targetNode = ProtocolTreeNode("message", {"form": "abc", "to":"xyz"}, [ProtocolTreeNode("media", {"width" : "123"}, data="123456")])
        self.assertEqual(node, targetNode)
