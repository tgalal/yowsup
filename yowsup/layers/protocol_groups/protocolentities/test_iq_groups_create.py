from .iq_groups_create import CreateGroupsIqProtocolEntity
from .test_iq_groups import GroupsIqProtocolEntityTest
from yowsup.structs import ProtocolTreeNode

class CreateGroupsIqProtocolEntityTest(GroupsIqProtocolEntityTest):
    def setUp(self):
        super(CreateGroupsIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = CreateGroupsIqProtocolEntity
        groupNode = ProtocolTreeNode("group", {"action": "create", "subject": "group_subj"})
        self.node.addChild(groupNode)