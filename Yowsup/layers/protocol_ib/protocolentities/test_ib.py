from .ib import IbProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest

class IbProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = IbProtocolEntity
        self.node = ProtocolTreeNode("ib")