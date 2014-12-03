from yowsup.layers.protocol_chatstate.protocolentities.chatstate_outgoing import OutgoingChatstateProtocolEntity
from yowsup.layers.protocol_chatstate.protocolentities.test_chatstate import ChatstateProtocolEntityTest

class OutgoingChatstateProtocolEntityTest(ChatstateProtocolEntityTest):
    def setUp(self):
        super(OutgoingChatstateProtocolEntityTest, self).setUp()
        self.ProtocolEntity = OutgoingChatstateProtocolEntity
        self.node.setAttribute("to", "chatstate_to")
