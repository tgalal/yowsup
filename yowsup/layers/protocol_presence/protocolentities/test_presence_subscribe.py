from yowsup.layers.protocol_presence.protocolentities.presence_subscribe import SubscribePresenceProtocolEntity
from yowsup.layers.protocol_presence.protocolentities.test_presence import PresenceProtocolEntityTest

class SubscribePresenceProtocolEntityTest(PresenceProtocolEntityTest):
    def setUp(self):
        super(SubscribePresenceProtocolEntityTest, self).setUp()
        self.ProtocolEntity = SubscribePresenceProtocolEntity
        self.node.setAttribute("type", "subscribe")
        self.node.setAttribute("to", "subscribe_jid")