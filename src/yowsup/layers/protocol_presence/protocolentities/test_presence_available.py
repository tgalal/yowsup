from .presence_available import AvailablePresenceProtocolEntity
from .test_presence import PresenceProtocolEntityTest

class AvailablePresenceProtocolEntityTest(PresenceProtocolEntityTest):
    def setUp(self):
        super(AvailablePresenceProtocolEntityTest, self).setUp()
        self.ProtocolEntity = AvailablePresenceProtocolEntity
        self.node.setAttribute("type", "available")
