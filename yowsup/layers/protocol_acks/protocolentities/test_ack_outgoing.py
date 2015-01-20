from yowsup.layers.protocol_acks.protocolentities.ack_outgoing import OutgoingAckProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

entity = OutgoingAckProtocolEntity("12345", "receipt", "delivery")

class OutgoingAckProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = OutgoingAckProtocolEntity
        self.node = entity.toProtocolTreeNode()