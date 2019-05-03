from yowsup.layers.protocol_media.protocolentities.test_message_media import MediaMessageProtocolEntityTest
from yowsup.layers.protocol_media.protocolentities import ExtendedTextMediaMessageProtocolEntity
from yowsup.layers.protocol_messages.proto.e2e_pb2 import Message


class ExtendedTextMediaMessageProtocolEntityTest(MediaMessageProtocolEntityTest):
    def setUp(self):
        super(ExtendedTextMediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = ExtendedTextMediaMessageProtocolEntity

        m = Message()
        media_message = Message.ExtendedTextMessage()
        media_message.canonical_url = "url"
        media_message.text = "text"
        media_message.matched_text = "matched_text"
        media_message.description = "desc"
        media_message.title = "title"
        media_message.jpeg_thumbnail = b"thumb"
        m.extended_text_message.MergeFrom(media_message)

        proto_node = self.node.getChild("proto")
        proto_node["mediatype"] = "url"
        proto_node.setData(m.SerializeToString())

        self._entity = ExtendedTextMediaMessageProtocolEntity\
            .fromProtocolTreeNode(self.node)  # type: ExtendedTextMediaMessageProtocolEntity

    def test_properties(self):
        self.assertEqual("url", self._entity.canonical_url)
        self.assertEqual("text", self._entity.text)
        self.assertEqual("matched_text", self._entity.matched_text)
        self.assertEqual("desc", self._entity.description)
        self.assertEqual("title", self._entity.title)
        self.assertEqual(b"thumb", self._entity.jpeg_thumbnail)
