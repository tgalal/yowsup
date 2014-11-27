from yowsup.layers.protocol_presence.protocolentities.presence_unavailable import UnavailablePresenceProtocolEntity
from yowsup.layers.protocol_presence.protocolentities.test_presence import PresenceProtocolEntityTest

class UnavailablePresenceProtocolEntityTest(PresenceProtocolEntityTest):
    def setUp(self):
        super(UnavailablePresenceProtocolEntityTest, self).setUp()
        self.ProtocolEntity = UnavailablePresenceProtocolEntity
        self.node.setAttribute("type", "unavailable")
