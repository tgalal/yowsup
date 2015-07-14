from yowsup.layers.protocol_acks.protocolentities.ack_incoming import IncomingAckProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest
import time

entity = IncomingAckProtocolEntity("12345", "message", "sender@s.whatsapp.com", int(time.time()))

class IncomingAckProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = IncomingAckProtocolEntity
        self.node = entity.toProtocolTreeNode()
