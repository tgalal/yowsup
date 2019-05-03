from yowsup.layers.protocol_media.protocolentities.message_media import MediaMessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities.test_message import MessageProtocolEntityTest
from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_messages.proto.e2e_pb2 import Message


class MediaMessageProtocolEntityTest(MessageProtocolEntityTest):
    def setUp(self):
        super(MediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = MediaMessageProtocolEntity
        proto_node = ProtocolTreeNode("proto", {"mediatype": "image"}, None, Message().SerializeToString())
        self.node.addChild(proto_node)
