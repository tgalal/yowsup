from yowsup.layers.protocol_messages.protocolentities.message_text import TextMessageProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_messages.protocolentities.test_message import MessageProtocolEntityTest
from yowsup.layers.protocol_messages.proto.e2e_pb2 import Message


class TextMessageProtocolEntityTest(MessageProtocolEntityTest):
    def setUp(self):
        super(TextMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = TextMessageProtocolEntity
        m = Message()
        m.conversation = "body_data"
        proto_node = ProtocolTreeNode("proto", {}, None, m.SerializeToString())
        self.node.addChild(proto_node)
