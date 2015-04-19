from yowsup.layers.protocol_media.protocolentities.message_media_downloadable_audio import AudioDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities.test_message_media_downloadable import DownloadableMediaMessageProtocolEntityTest

class AudioDownloadableMediaMessageProtocolEntityTest(DownloadableMediaMessageProtocolEntityTest):
    def setUp(self):
        super(AudioDownloadableMediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = AudioDownloadableMediaMessageProtocolEntity
        mediaNode = self.node.getChild("media")
        mediaNode.setAttribute("abitrate", "31")
        mediaNode.setAttribute("acodec", "aac")
        mediaNode.setAttribute("asampfreq", "22050")
        mediaNode.setAttribute("duration", "3")
        mediaNode.setAttribute("encoding", "raw")
        mediaNode.setAttribute("origin", "live")
        mediaNode.setAttribute("seconds", "3")
