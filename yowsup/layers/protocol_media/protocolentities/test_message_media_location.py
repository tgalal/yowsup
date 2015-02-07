from yowsup.layers.protocol_media.protocolentities import LocationMediaMessageProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest
class LocationMediaMessageProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = LocationMediaMessageProtocolEntity
        self.xml = """
            <message t="1234" from="{{CONTACT_JID}}"
                offline="1" type="media" id="1234" notify="{{NOTIFY_NAME}}">
                <media
                    latitude="52.52393"
                    type="location"
                    longitude="13.41747"
                    name="Location Name"
                    url="http://www.foursquare.com/XXXX"
                    encoding="raw"
                >{{THUMBNAIL_RAWDATA}}</media>
            </message>
            """