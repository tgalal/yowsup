from yowsup.layers.protocol_media.protocolentities.message_media_downloadable import DownloadableMediaMessageProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest
class DownloadableMediaMessageProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = DownloadableMediaMessageProtocolEntity
        self.xml = """
            <message t="123456" from="jid"
                offline="1" type="media" id="1234" notify="notify">
                <media type="audio"
                    mimetype="image/jpeg"
                    filehash="FILE_HASH"
                    url="DOWNLOAD_URL"
                    ip="IP"
                    size="12345"
                    file="FILENAME">
                    PREVIEW
                </media>
            </message>
        """
