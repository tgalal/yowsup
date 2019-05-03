from yowsup.layers.protocol_media.protocolentities.test_message_media import MediaMessageProtocolEntityTest
from yowsup.layers.protocol_media.protocolentities import LocationMediaMessageProtocolEntity
from yowsup.layers.protocol_messages.proto.e2e_pb2 import Message


class LocationMediaMessageProtocolEntityTest(MediaMessageProtocolEntityTest):
    def setUp(self):
        super(LocationMediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = LocationMediaMessageProtocolEntity

        m = Message()
        location_message = Message.LocationMessage()
        location_message.degrees_latitude = 30.089037
        location_message.degrees_longitude = 31.319488
        location_message.name = "kaos"
        location_message.url = "kaos_url"

        m.location_message.MergeFrom(location_message)

        proto_node = self.node.getChild("proto")
        proto_node["mediatype"] = "location"
        proto_node.setData(m.SerializeToString())