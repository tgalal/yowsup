from yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest
from yowsup.layers.protocol_iq.protocolentities import ErrorIqProtocolEntity
from yowsup.structs import ProtocolTreeNode

class ErrorIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(ErrorIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = ErrorIqProtocolEntity
        errorNode = ProtocolTreeNode("error", {"code": "123", "text": "abc"})
        self.node.addChild(errorNode)
