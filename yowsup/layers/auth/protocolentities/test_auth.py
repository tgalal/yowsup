from yowsup.layers.auth.protocolentities import AuthProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class AuthProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = AuthProtocolEntity 
        self.node = ProtocolTreeNode("auth", {"user": "testuser", "mechanism": "WAUTH-2", "passive": "false"})