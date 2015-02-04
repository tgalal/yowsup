from yowsup.layers.protocol_receipts.protocolentities import OutgoingReceiptProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class OutgoingReceiptProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = OutgoingReceiptProtocolEntity
        self.node = OutgoingReceiptProtocolEntity("123", "target", "read").toProtocolTreeNode()