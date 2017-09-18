from yowsup.layers.protocol_media.protocolentities.test_message_media import MediaMessageProtocolEntityTest
from yowsup.layers.protocol_media.protocolentities import VCardMediaMessageProtocolEntity
from yowsup.structs import ProtocolTreeNode
class VCardMediaMessageProtocolEntityTest(MediaMessageProtocolEntityTest):
    def setUp(self):
        super(VCardMediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = VCardMediaMessageProtocolEntity
        vcardNode = ProtocolTreeNode("vcard", {"name":"abc"}, None, "VCARD_DATA")
        mediaNode = self.node.getChild("media")
        mediaNode["type"] = "vcard"
        mediaNode.addChild(vcardNode)
