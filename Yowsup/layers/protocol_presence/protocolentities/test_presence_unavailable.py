from .presence_unavailable import UnavailablePresenceProtocolEntity
from .test_presence import PresenceProtocolEntityTest

class UnavailablePresenceProtocolEntityTest(PresenceProtocolEntityTest):
    def setUp(self):
        super(UnavailablePresenceProtocolEntityTest, self).setUp()
        self.ProtocolEntity = UnavailablePresenceProtocolEntity
        self.node.setAttribute("type", "unavailable")
