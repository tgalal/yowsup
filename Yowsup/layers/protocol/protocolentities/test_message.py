from .message import MessageProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest

class MessageProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = MessageProtocolEntity
        attribs = {
            "t": "12345",
            "from": "from_jid",
            "offline": "0",
            "type": "text",
            "id": "message-id",
            "notify": "notify_name"
        }
        self.node = ProtocolTreeNode("message", attribs)