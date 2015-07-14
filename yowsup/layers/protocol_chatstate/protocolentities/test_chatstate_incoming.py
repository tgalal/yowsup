from yowsup.layers.protocol_chatstate.protocolentities.chatstate_incoming import IncomingChatstateProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

entity = IncomingChatstateProtocolEntity(IncomingChatstateProtocolEntity.STATE_TYPING, "jid@s.whatsapp.net")

class IncomingChatstateProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = IncomingChatstateProtocolEntity
        self.node = entity.toProtocolTreeNode()
