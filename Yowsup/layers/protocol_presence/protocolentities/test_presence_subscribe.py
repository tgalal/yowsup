from .presence_subscribe import SubscribePresenceProtocolEntity
from .test_presence import PresenceProtocolEntityTest

class SubscribePresenceProtocolEntityTest(PresenceProtocolEntityTest):
    def setUp(self):
        super(SubscribePresenceProtocolEntityTest, self).setUp()
        self.ProtocolEntity = SubscribePresenceProtocolEntity
        self.node.setAttribute("type", "subscribe")
        self.node.setAttribute("to", "subscribe_jid")