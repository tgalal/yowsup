from yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest
from yowsup.layers.protocol_profiles.protocolentities import UnregisterIqProtocolEntity
from yowsup.structs import ProtocolTreeNode

class UnregisterIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(UnregisterIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = UnregisterIqProtocolEntity
        self.node.addChild(ProtocolTreeNode("remove", {"xmlns": "urn:xmpp:whatsapp:account"}))