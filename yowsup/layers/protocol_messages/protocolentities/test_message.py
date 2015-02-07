from yowsup.layers.protocol_messages.protocolentities.message import MessageProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class MessageProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = MessageProtocolEntity
        attribs = {
            "type": "text",
            "id": "message-id",
            "t": "12345",
            "offline": "0",
            "from": "from_jid",
            "notify": "notify_name"
        }
        self.node = ProtocolTreeNode("message", attribs)

