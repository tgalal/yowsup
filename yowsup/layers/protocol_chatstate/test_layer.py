from yowsup.layers import YowProtocolLayerTest
from yowsup.layers.protocol_chatstate import YowChatstateProtocolLayer
from yowsup.layers.protocol_chatstate.protocolentities import IncomingChatstateProtocolEntity, OutgoingChatstateProtocolEntity

class YowChatStateProtocolLayerTest(YowProtocolLayerTest, YowChatstateProtocolLayer):
    def setUp(self):
        YowChatstateProtocolLayer.__init__(self)

    def test_send(self):
        entity = OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_PAUSED, "jid@s.whatsapp.net")
        self.assertSent(entity)

    def test_receive(self):
        entity = IncomingChatstateProtocolEntity(IncomingChatstateProtocolEntity.STATE_TYPING, "jid@s.whatsapp.net")
        self.assertReceived(entity)