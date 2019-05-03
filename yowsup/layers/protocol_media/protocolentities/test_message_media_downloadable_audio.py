from yowsup.layers.protocol_media.protocolentities.message_media_downloadable_audio import AudioDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_messages.proto.e2e_pb2 import Message
from .test_message_media import MediaMessageProtocolEntityTest


class AudioDownloadableMediaMessageProtocolEntityTest(MediaMessageProtocolEntityTest):
    def setUp(self):
        super(AudioDownloadableMediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = AudioDownloadableMediaMessageProtocolEntity
        proto_node = self.node.getChild("proto")
        m = Message()
        media_message = Message.AudioMessage()
        media_message.url = "url"
        media_message.mimetype = "audio/ogg"
        media_message.file_sha256 = b"SHA256"
        media_message.file_length = 123
        media_message.media_key = b"MEDIA_KEY"
        media_message.seconds = 24
        media_message.ptt = True
        m.audio_message.MergeFrom(media_message)
        proto_node.setData(m.SerializeToString())
