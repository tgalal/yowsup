from yowsup.layers.protocol_media.protocolentities.message_media_downloadable_video import VideoDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities.test_message_media_downloadable import DownloadableMediaMessageProtocolEntityTest

class VideoDownloadableMediaMessageProtocolEntityTest(DownloadableMediaMessageProtocolEntityTest):
    def setUp(self):
        super(VideoDownloadableMediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = VideoDownloadableMediaMessageProtocolEntity
        mediaNode = self.node.getChild("media")
        mediaNode.setAttribute("abitrate",  "165")
        mediaNode.setAttribute("acodec",    "aac")
        mediaNode.setAttribute("asampfmt",  "flt")
        mediaNode.setAttribute("asampfreq", "48000")
        mediaNode.setAttribute("duration",  "61")
        mediaNode.setAttribute("encoding",  "raw")
        mediaNode.setAttribute("fps",       "24")
        mediaNode.setAttribute("height",    "452")
        mediaNode.setAttribute("seconds",   "61")
        mediaNode.setAttribute("vbitrate",  "1862")
        mediaNode.setAttribute("vcodec",    "h264")
        mediaNode.setAttribute("width",     "800")
