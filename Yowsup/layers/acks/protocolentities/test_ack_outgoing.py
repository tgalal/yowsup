from .ack_outgoing import OutgoingAckProtocolEntity
from .test_ack import AckProtocolEntityTest
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest

class OutgoingAckProtocolEntityTest(AckProtocolEntityTest):
    def setUp(self):
        super(OutgoingAckProtocolEntityTest, self).setUp()
        self.ProtocolEntity = OutgoingAckProtocolEntity
        self.node.setAttribute("type", "ack_type")
