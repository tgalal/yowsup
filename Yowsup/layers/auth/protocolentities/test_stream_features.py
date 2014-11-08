from .stream_features import StreamFeaturesProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest

class StreamFeaturesProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = StreamFeaturesProtocolEntity
        attribs = {
        }
        childNode = ProtocolTreeNode("receipt_acks", {}, None, None)
        self.node = ProtocolTreeNode("stream:features", attribs, [childNode])