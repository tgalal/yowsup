from .groupmessage_text import TextGroupMessageProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest

class TextGroupMessageProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        super(TextGroupMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = TextGroupMessageProtocolEntity
        bodyNode = ProtocolTreeNode("body", {}, None, "body_data")
        self.node.addChild(bodyNode)
