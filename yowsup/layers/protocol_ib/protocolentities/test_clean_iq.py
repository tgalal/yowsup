from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_ib.protocolentities.clean_iq import CleanIqProtocolEntity
from yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest

class CleanIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(CleanIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = CleanIqProtocolEntity
        cleanNode = ProtocolTreeNode("clean", {"type": "groups"})
        self.node.addChild(cleanNode)