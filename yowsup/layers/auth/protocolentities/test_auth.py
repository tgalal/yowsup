from yowsup.layers.auth.protocolentities import AuthProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
from yowsup.structs import ProtocolTreeNode
import unittest

class AuthProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = AuthProtocolEntity 
        self.xml = '<auth passive="false" user="0123456789" mechanism="WAUTH-2">blob</auth>'
