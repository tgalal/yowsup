from yowsup.layers.auth.protocolentities.response import ResponseProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class ResponseProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = ResponseProtocolEntity
        self.xml = '<response xmlns="urn:ietf:params:xml:ns:xmpp-sasl">aaaa</response>'
        self.node = ResponseProtocolEntity("aaaa").toProtocolTreeNode()