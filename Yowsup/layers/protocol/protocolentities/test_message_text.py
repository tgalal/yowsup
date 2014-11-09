from .message_text import TextMessageProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest

class TextMessageProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        super(TextMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = TextMessageProtocolEntity
        bodyNode = ProtocolTreeNode("body", {}, None, "body_data")
        self.node.addChild(bodyNode)
