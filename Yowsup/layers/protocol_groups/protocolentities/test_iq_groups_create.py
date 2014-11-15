from .iq_groups_create import CreateGroupsIqProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest

class CreateGroupsIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(CreateGroupsIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = CreateGroupsIqProtocolEntity
        groupNode = ProtocolTreeNode("group", {"action": "create", "subject": "group_subj"})
        self.node.addChild(groupNode)