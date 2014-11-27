from yowsup.layers.protocol_acks.protocolentities.ack_outgoing import OutgoingAckProtocolEntity
from yowsup.layers.protocol_acks.protocolentities.test_ack import AckProtocolEntityTest

class OutgoingAckProtocolEntityTest(AckProtocolEntityTest):
    def setUp(self):
        super(OutgoingAckProtocolEntityTest, self).setUp()
        self.ProtocolEntity = OutgoingAckProtocolEntity
        self.node.setAttribute("type", "ack_type")
