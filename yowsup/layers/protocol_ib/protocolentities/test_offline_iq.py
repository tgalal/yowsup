from yowsup.layers.protocol_ib.protocolentities.test_ib import IbProtocolEntityTest
from yowsup.layers.protocol_ib.protocolentities.offline_ib import OfflineIbProtocolEntity
from yowsup.structs import ProtocolTreeNode
class OfflineIbProtocolEntityTest(IbProtocolEntityTest):
    def setUp(self):
        super(OfflineIbProtocolEntityTest, self).setUp()
        self.ProtocolEntity = OfflineIbProtocolEntity
        self.node.addChild(ProtocolTreeNode("offline", {"count": "5"}))