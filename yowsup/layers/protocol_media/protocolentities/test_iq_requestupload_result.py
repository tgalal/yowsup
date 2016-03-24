from yowsup.layers.protocol_iq.protocolentities.test_iq_result import ResultIqProtocolEntityTest
from yowsup.layers.protocol_media.protocolentities import ResultRequestUploadIqProtocolEntity
from yowsup.structs import ProtocolTreeNode


class ResultRequestUploadIqProtocolEntityTest(ResultIqProtocolEntityTest):
    def setUp(self):
        super(ResultRequestUploadIqProtocolEntityTest, self).setUp()
        mediaNode = ProtocolTreeNode("media", {"url": "url", "ip": "1.2.3.4"})
        self.ProtocolEntity = ResultRequestUploadIqProtocolEntity
        self.node.addChild(mediaNode)
