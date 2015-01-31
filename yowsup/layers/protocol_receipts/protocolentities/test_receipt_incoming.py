from yowsup.layers.protocol_receipts.protocolentities import IncomingReceiptProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest
import time

class IncomingReceiptProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = IncomingReceiptProtocolEntity
        self.node = IncomingReceiptProtocolEntity("123", "sender", int(time.time())).toProtocolTreeNode()
