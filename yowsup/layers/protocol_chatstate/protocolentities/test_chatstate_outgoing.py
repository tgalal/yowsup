from yowsup.layers.protocol_chatstate.protocolentities.chatstate_outgoing import OutgoingChatstateProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

entity = OutgoingChatstateProtocolEntity(OutgoingChatstateProtocolEntity.STATE_PAUSED, "jid@s.whatsapp.net")

class OutgoingChatstateProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = OutgoingChatstateProtocolEntity
        self.node = entity.toProtocolTreeNode()
