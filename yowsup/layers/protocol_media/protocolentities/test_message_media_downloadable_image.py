from yowsup.layers.protocol_media.protocolentities.message_media_downloadable_image import ImageDownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities.test_message_media_downloadable import DownloadableMediaMessageProtocolEntityTest

class ImageDownloadableMediaMessageProtocolEntityTest(DownloadableMediaMessageProtocolEntityTest):
    def setUp(self):
        super(ImageDownloadableMediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = ImageDownloadableMediaMessageProtocolEntity
        mediaNode = self.node.getChild("media")
        mediaNode.setAttribute("encoding",  "ENCODING")
        mediaNode.setAttribute("width",     "1024")
        mediaNode.setAttribute("height",     "768")
        mediaNode.setAttribute("caption", "caption")
