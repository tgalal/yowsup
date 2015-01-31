from yowsup.layers.protocol_media.protocolentities import ResultRequestUploadIqProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import  unittest
class ResultRequestUploadIqProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = ResultRequestUploadIqProtocolEntity
        self.xml = """
        <iq id="1" from="s.whatsapp.net" type="result">
            <duplicate mimetype="image/jpeg" width="672" type="image" size="52223" url="image_url" height="896" filehash="file_hash"/>
        </iq>
        """
