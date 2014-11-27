from yowsup.layers.protocol_groups.protocolentities.iq_result_groups_list import ListGroupsResultIqProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities.test_iq_result import ResultIqProtocolEntityTest

class ListGroupsResultIqProtocolEntityTest(ResultIqProtocolEntityTest):
    def setUp(self):
        super(ListGroupsResultIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = ListGroupsResultIqProtocolEntity
        # groups = [
        #     Group("GROUPID", "OWNERJID", "SUBJ", "SUBJECT_OWNER", time.time(), time.time()),
        #     Group("GROUP2ID", "OWNER2JID", "SUBJ2", "SUBJECT2_OWNER", time.time(), time.time())
        # ]

        groupNode1 = ProtocolTreeNode("group", {
            "id": "GROUP_ID",
            "owner": "group_onwer",
            "subject": "SUBJECT",
            "s_o": "SUBJECT_OWNER",
            "s_t": "1234567",
            "creation": "1234567"
        })
        groupNode2 = ProtocolTreeNode("group", {
            "id": "GROUP_ID2",
            "owner": "group_onwer2",
            "subject": "SUBJECT2",
            "s_o": "SUBJECT_OWNER2",
            "s_t": "1234567",
            "creation": "1234567"
        })

        self.node.addChildren([groupNode1, groupNode2])
