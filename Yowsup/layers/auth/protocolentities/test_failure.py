from .failure import FailureProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest

class FailureProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = FailureProtocolEntity
        self.node = ProtocolTreeNode("failure", {}, [ProtocolTreeNode("not-authorized", {})])