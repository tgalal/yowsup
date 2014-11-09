from .groupmessage  import GroupMessageProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest
from Yowsup.layers.messages.protocolentities.test_message import MessageProtocolEntityTest

class GroupMessageProtocolEntityTest(MessageProtocolEntityTest):
    def setUp(self):
        super(GroupMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = GroupMessageProtocolEntity
        self.node.setAttribute("participant", "participant_jid")