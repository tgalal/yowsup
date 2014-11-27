from yowsup.layers.auth.protocolentities.failure import FailureProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest

class FailureProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = FailureProtocolEntity
        self.node = ProtocolTreeNode("failure", {}, [ProtocolTreeNode("not-authorized", {})])