from .presence_unsubscribe import UnsubscribePresenceProtocolEntity
from .test_presence import PresenceProtocolEntityTest

class UnsubscribePresenceProtocolEntityTest(PresenceProtocolEntityTest):
    def setUp(self):
        super(UnsubscribePresenceProtocolEntityTest, self).setUp()
        self.ProtocolEntity = UnsubscribePresenceProtocolEntity
        self.node.setAttribute("type", "unsubscribe")
        self.node.setAttribute("to", "some_jid")