from .iq_group_create import CreateGroupIqProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest

class CreateGroupIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(CreateGroupIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = CreateGroupIqProtocolEntity
        groupNode = ProtocolTreeNode("group", {"action": "create", "subject": "group_subj"})
        self.node.addChild(groupNode)