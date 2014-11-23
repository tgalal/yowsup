from .message_text import TextMessageProtocolEntity
from yowsup.structs import ProtocolTreeNode
from .test_message import MessageProtocolEntityTest

class TextMessageProtocolEntityTest(MessageProtocolEntityTest):
    def setUp(self):
        super(TextMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = TextMessageProtocolEntity
        bodyNode = ProtocolTreeNode("body", {}, None, "body_data")
        self.node.addChild(bodyNode)
