from yowsup.layers.protocol_ib.protocolentities.ib import IbProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest

class IbProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = IbProtocolEntity
        self.node = ProtocolTreeNode("ib")
