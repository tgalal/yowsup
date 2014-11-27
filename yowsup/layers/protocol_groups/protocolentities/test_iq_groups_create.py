from yowsup.layers.protocol_groups.protocolentities.iq_groups_create import CreateGroupsIqProtocolEntity
from yowsup.layers.protocol_groups.protocolentities.test_iq_groups import GroupsIqProtocolEntityTest
from yowsup.structs import ProtocolTreeNode

class CreateGroupsIqProtocolEntityTest(GroupsIqProtocolEntityTest):
    def setUp(self):
        super(CreateGroupsIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = CreateGroupsIqProtocolEntity
        groupNode = ProtocolTreeNode("group", {"action": "create", "subject": "group_subj"})
        self.node.addChild(groupNode)