from yowsup.layers.protocol_media.protocolentities.message_media_downloadable_image \
    import ImageDownloadableMediaMessageProtocolEntity
from .test_message_media import MediaMessageProtocolEntityTest
from yowsup.layers.protocol_messages.proto.e2e_pb2 import Message


class ImageDownloadableMediaMessageProtocolEntityTest(MediaMessageProtocolEntityTest):
    def setUp(self):
        super(ImageDownloadableMediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = ImageDownloadableMediaMessageProtocolEntity
        proto_node = self.node.getChild("proto")
        m = Message()
        media_message = Message.ImageMessage()
        media_message.url = "url"
        media_message.mimetype = "image/jpeg"
        media_message.caption = "caption"
        media_message.file_sha256 = b"SHA256"
        media_message.file_length = 123
        media_message.height = 20
        media_message.width = 20
        media_message.media_key = b"MEDIA_KEY"
        media_message.jpeg_thumbnail = b"THUMBNAIL"
        m.image_message.MergeFrom(media_message)
        proto_node.setData(m.SerializeToString())
