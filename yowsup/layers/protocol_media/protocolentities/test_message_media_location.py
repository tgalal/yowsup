from yowsup.layers.protocol_media.protocolentities.test_message_media import MediaMessageProtocolEntityTest
from yowsup.layers.protocol_media.protocolentities import LocationMediaMessageProtocolEntity
from yowsup.structs import ProtocolTreeNode
class LocationMediaMessageProtocolEntityTest(MediaMessageProtocolEntityTest):
    def setUp(self):
        super(LocationMediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = LocationMediaMessageProtocolEntity
        mediaNode = self.node.getChild("media")
        mediaNode["type"] = "location"
        mediaNode["latitude"] = "52.52393"
        mediaNode["longitude"] = "13.41747"
        mediaNode["encoding"] = "raw"
