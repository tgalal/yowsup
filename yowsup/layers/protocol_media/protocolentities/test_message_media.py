from yowsup.layers.protocol_media.protocolentities.message_media import MediaMessageProtocolEntity
import unittest
from yowsup.structs.protocolentity import ProtocolEntityTest

class MediaMessageProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        super(MediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = MediaMessageProtocolEntity
        self.xml = """
        <message participant="participant" t="123456" from="sender" offline="0" type="media" id="ID" notify="notify">
            <media type="image">preview</media>
        </message>
        """
