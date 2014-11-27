from yowsup.layers.protocol_acks.protocolentities.ack import AckProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest

class AckProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = AckProtocolEntity
        self.node = ProtocolTreeNode("ack", {"id": "test_id", "class": "ack_class"}, None, None)
