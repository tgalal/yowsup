from yowsup.layers.protocol_media.protocolentities import RequestUploadIqProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest
class RequestUploadIqProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = RequestUploadIqProtocolEntity
        self.xml = """
            <iq id="1234" to="s.whatsapp.net" type="set" xmlns="w:m">
                <media hash="qwerty" type="image" size="12345" orighash="qwerty"></media>
            </iq>"""
