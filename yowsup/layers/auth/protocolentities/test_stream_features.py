from yowsup.layers.auth.protocolentities.stream_features import StreamFeaturesProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class StreamFeaturesProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = StreamFeaturesProtocolEntity
        attribs = {
        }
        childNode = ProtocolTreeNode("receipt_acks", {}, None, None)
        self.node = ProtocolTreeNode("stream:features", attribs, [childNode])