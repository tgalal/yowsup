from .iq import IqProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest

class IqProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = IqProtocolEntity
        self.node = ProtocolTreeNode("iq", {"id": "test_id", "type": "get", "xmlns": "iq_xmlns"}, None, None)