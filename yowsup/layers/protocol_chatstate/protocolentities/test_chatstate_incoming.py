from yowsup.layers.protocol_chatstate.protocolentities.chatstate_incoming import IncomingChatstateProtocolEntity
from yowsup.layers.protocol_chatstate.protocolentities.test_chatstate import ChatstateProtocolEntityTest

class IncomingChatstateProtocolEntityTest(ChatstateProtocolEntityTest):
    def setUp(self):
        super(IncomingChatstateProtocolEntityTest, self).setUp()
        self.ProtocolEntity = IncomingChatstateProtocolEntity
        self.node.setAttribute("from", "chatstate_from")
