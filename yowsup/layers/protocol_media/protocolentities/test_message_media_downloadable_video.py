from yowsup.layers.protocol_media.protocolentities.message_media_downloadable_video \
    import VideoDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_messages.proto.e2e_pb2 import Message
from .test_message_media import MediaMessageProtocolEntityTest


class VideoDownloadableMediaMessageProtocolEntityTest(MediaMessageProtocolEntityTest):
    def setUp(self):
        super(VideoDownloadableMediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = VideoDownloadableMediaMessageProtocolEntity
        proto_node = self.node.getChild("proto")
        m = Message()
        media_message = Message.VideoMessage()
        media_message.url = "url"
        media_message.mimetype = "video/mp4"
        media_message.caption = "caption"
        media_message.file_sha256 = b"SHA256"
        media_message.file_length = 123
        media_message.height = 20
        media_message.width = 20
        media_message.media_key = b"MEDIA_KEY"
        media_message.jpeg_thumbnail = b"THUMBNAIL"
        m.video_message.MergeFrom(media_message)
        proto_node.setData(m.SerializeToString())
