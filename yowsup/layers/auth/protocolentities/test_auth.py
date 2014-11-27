from yowsup.layers.auth.protocolentities import AuthProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest

class AuthProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = AuthProtocolEntity 
        self.node = ProtocolTreeNode("auth", {"user": "testuser", "mechanism": "WAUTH-2", "passive": "false"})