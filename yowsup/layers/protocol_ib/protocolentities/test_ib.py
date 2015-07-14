from yowsup.layers.protocol_ib.protocolentities.ib import IbProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class IbProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = IbProtocolEntity
        self.node = ProtocolTreeNode("ib")
