from yowsup.layers.auth.protocolentities.stream_features import StreamFeaturesProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class StreamFeaturesProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = StreamFeaturesProtocolEntity
        self.xml = '<stream:features xmlns:stream="stream"><readreceipts /></stream:features>'
