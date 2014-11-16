from .iq_groups_list import ListGroupsIqProtocolEntity
from .test_iq_groups import GroupsIqProtocolEntityTest
from Yowsup.structs import ProtocolTreeNode

class ListGroupsIqProtocolEntityTest(GroupsIqProtocolEntityTest):
    def setUp(self):
        super(ListGroupsIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = ListGroupsIqProtocolEntity
        groupNode = ProtocolTreeNode("list", {"type": "participating"})
        self.node.addChild(groupNode)