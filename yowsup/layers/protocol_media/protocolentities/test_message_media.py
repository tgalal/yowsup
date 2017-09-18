from yowsup.layers.protocol_media.protocolentities.message_media import MediaMessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities.test_message import MessageProtocolEntityTest
from yowsup.structs import ProtocolTreeNode

class MediaMessageProtocolEntityTest(MessageProtocolEntityTest):
    def setUp(self):
        super(MediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = MediaMessageProtocolEntity
        mediaNode = ProtocolTreeNode("media", {"type":"MEDIA_TYPE"}, None, None)
        self.node.addChild(mediaNode)
