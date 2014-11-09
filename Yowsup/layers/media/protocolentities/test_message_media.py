from .message_media import MediaMessageProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest

class MediaMessageProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        super(MediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = MediaMessageProtocolEntity
        mediaNode = ProtocolTreeNode("media", {"type":"MEDIA_TYPE"}, None, None)
        self.node.addChild(mediaNode)
