from .message import MessageProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest

class MessageProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = MessageProtocolEntity
        # ORDER_MATTERS for node.toString() to output return attribs in same order
        attribs = {
            "type": "message_type",
            "id": "message-id",
            "t": "12345",
            "offline": "0",
            "from": "from_jid",
            "notify": "notify_name"
        }
        self.node = ProtocolTreeNode("message", attribs)

