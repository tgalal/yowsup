from .message_text_group import GroupTextMessageProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest

class GroupTextMessageProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        super(GroupTextMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = GroupTextMessageProtocolEntity
        self.node.setAttribute("participant", "participant_jid")