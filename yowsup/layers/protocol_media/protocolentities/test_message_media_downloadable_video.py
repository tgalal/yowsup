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
        media_message.file_sha256 = b"shaval"
        media_message.file_length = 4
        media_message.width = 1
        media_message.height = 2
        media_message.seconds = 3
        media_message.media_key = b"MEDIA_KEY"
        media_message.jpeg_thumbnail = b"THUMBNAIL"
        media_message.gif_attribution = 0
        media_message.gif_playback = False
        media_message.streaming_sidecar = b''
        m.video_message.MergeFrom(media_message)
        proto_node.setData(m.SerializeToString())
