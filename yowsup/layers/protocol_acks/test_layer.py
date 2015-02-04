from yowsup.layers import YowProtocolLayerTest
from yowsup.layers.protocol_acks import YowAckProtocolLayer
from yowsup.layers.protocol_acks.protocolentities.test_ack_incoming import entity as incomingAckEntity
from yowsup.layers.protocol_acks.protocolentities.test_ack_outgoing import entity as outgoingAckEntity
class YowAckProtocolLayerTest(YowProtocolLayerTest, YowAckProtocolLayer):
    def setUp(self):
        YowAckProtocolLayer.__init__(self)

    def test_receive(self):
        self.assertReceived(incomingAckEntity)

    def test_send(self):
        self.assertSent(outgoingAckEntity)
