from .message_media_downloadable_image import ImageDownloadableMediaMessageProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest
from .test_message_media_downloadable import DownloadableMediaMessageProtocolEntityTest

class ImageDownloadableMediaMessageProtocolEntityTest(DownloadableMediaMessageProtocolEntityTest):
    def setUp(self):
        super(ImageDownloadableMediaMessageProtocolEntityTest, self).setUp()
        self.ProtocolEntity = ImageDownloadableMediaMessageProtocolEntity
        mediaNode = self.node.getChild("media")
        mediaNode.setAttribute("encoding",  "ENCODING")
        mediaNode.setAttribute("width",     "1024")
        mediaNode.setAttribute("height",     "768")
