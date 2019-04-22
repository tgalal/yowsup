from yowsup.layers.auth.protocolentities.success import SuccessProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest


class SuccessProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = SuccessProtocolEntity
        attribs = {
            "creation": "1234",
            "location": "atn",
            "props": "2",
            "t": "1415470561"
        }
        self.node = ProtocolTreeNode("success", attribs)
