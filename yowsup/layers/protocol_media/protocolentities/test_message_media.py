from yowsup.layers.protocol_media.protocolentities.message_media import MediaMessageProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest

class MediaMessageProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        super(MediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = MediaMessageProtocolEntity
        mediaNode = ProtocolTreeNode("media", {"type":"MEDIA_TYPE"}, None, None)
        self.node.addChild(mediaNode)
