from .ack import AckProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest

class AckProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = AckProtocolEntity
        self.node = ProtocolTreeNode("ack", {"id": "test_id", "class": "ack_class"}, None, None)
