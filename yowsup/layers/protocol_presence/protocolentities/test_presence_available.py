from yowsup.layers.protocol_presence.protocolentities.presence_available import AvailablePresenceProtocolEntity
from yowsup.layers.protocol_presence.protocolentities.test_presence import PresenceProtocolEntityTest

class AvailablePresenceProtocolEntityTest(PresenceProtocolEntityTest):
    def setUp(self):
        super(AvailablePresenceProtocolEntityTest, self).setUp()
        self.ProtocolEntity = AvailablePresenceProtocolEntity
        self.node.setAttribute("type", "available")
