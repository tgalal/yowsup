from yowsup.layers.protocol_calls.protocolentities.call import CallProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class CallProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = CallProtocolEntity
        children = [ProtocolTreeNode("offer", {"call-id": "call_id"})]
        attribs = {
            "t": "12345",
            "from": "from_jid",
            "offline": "0",
            "id": "message_id",
            "notify": "notify_name"
        }
        self.node = ProtocolTreeNode("call", attribs, children)
