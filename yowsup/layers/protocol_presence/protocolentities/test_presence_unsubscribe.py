from yowsup.layers.protocol_presence.protocolentities.presence_unsubscribe import UnsubscribePresenceProtocolEntity
from yowsup.layers.protocol_presence.protocolentities.test_presence import PresenceProtocolEntityTest

class UnsubscribePresenceProtocolEntityTest(PresenceProtocolEntityTest):
    def setUp(self):
        super(UnsubscribePresenceProtocolEntityTest, self).setUp()
        self.ProtocolEntity = UnsubscribePresenceProtocolEntity
        self.node.setAttribute("type", "unsubscribe")
        self.node.setAttribute("to", "some_jid")