from .test_ib import IbProtocolEntityTest
from .dirty_ib import DirtyIbProtocolEntity
from yowsup.structs import ProtocolTreeNode
class DirtyIbProtocolEntityTest(IbProtocolEntityTest):
    def setUp(self):
        super(DirtyIbProtocolEntityTest, self).setUp()
        self.ProtocolEntity = DirtyIbProtocolEntity
        dirtyNode = ProtocolTreeNode("dirty")
        dirtyNode["timestamp"] = "123456"
        dirtyNode["type"] = "groups"
        self.node.addChild(dirtyNode)