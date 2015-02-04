from yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest
from yowsup.layers.protocol_media.protocolentities import RequestUploadIqProtocolEntity
from yowsup.structs import ProtocolTreeNode
class RequestUploadIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(RequestUploadIqProtocolEntityTest, self).setUp()
        mediaNode = ProtocolTreeNode("media", {"hash": "hash", "size": "1234", "orighash": "orighash", "type": "image"})
        self.ProtocolEntity = RequestUploadIqProtocolEntity
        self.node.setAttribute("type", "set")
        self.node.addChild(mediaNode)