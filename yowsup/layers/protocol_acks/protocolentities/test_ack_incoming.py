from yowsup.layers.protocol_acks.protocolentities.ack_incoming import IncomingAckProtocolEntity
from yowsup.layers.protocol_acks.protocolentities.test_ack import AckProtocolEntityTest

class IncomingAckProtocolEntityTest(AckProtocolEntityTest):
    def setUp(self):
        super(IncomingAckProtocolEntityTest, self).setUp()
        self.ProtocolEntity = IncomingAckProtocolEntity
        self.node.setAttribute("from", "ack_from")
        self.node.setAttribute("t", "ack_timestamp")
