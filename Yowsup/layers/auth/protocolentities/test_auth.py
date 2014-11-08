from .auth import AuthProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest

class AuthProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = AuthProtocolEntity 
        self.node = ProtocolTreeNode("auth", {"user": "testuser", "mechanism": "WAUTH-2", "passive": "false"})