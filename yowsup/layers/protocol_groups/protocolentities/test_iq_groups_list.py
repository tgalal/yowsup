from yowsup.layers.protocol_groups.protocolentities.iq_groups_list import ListGroupsIqProtocolEntity
from yowsup.layers.protocol_groups.protocolentities.test_iq_groups import GroupsIqProtocolEntityTest
from yowsup.structs import ProtocolTreeNode

class ListGroupsIqProtocolEntityTest(GroupsIqProtocolEntityTest):
    def setUp(self):
        super(ListGroupsIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = ListGroupsIqProtocolEntity
        groupNode = ProtocolTreeNode("list", {"type": "participating"})
        self.node.addChild(groupNode)