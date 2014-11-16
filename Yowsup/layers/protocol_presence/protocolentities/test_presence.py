from .presence import PresenceProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest

class PresenceProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = PresenceProtocolEntity
        self.node = ProtocolTreeNode("presence", {"type": "presence_type", "name": "presence_name"}, None, None)
