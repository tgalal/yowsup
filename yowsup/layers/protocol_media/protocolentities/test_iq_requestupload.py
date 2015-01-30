from yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest
from yowsup.layers.protocol_media.protocolentities import RequestUploadIqProtocolEntity
from yowsup.structs import ProtocolTreeNode
class RequestUploadIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(RequestUploadIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = RequestUploadIqProtocolEntity
        self.xml = """
            <iq id="1234" to="s.whatsapp.net" type="set" xmlns="w:m">
                <media hash="qwerty" type="image" size="12345" orighash="qwerty"></media>
            </iq>"""