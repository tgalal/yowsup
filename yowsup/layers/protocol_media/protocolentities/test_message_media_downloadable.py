from yowsup.layers.protocol_media.protocolentities.message_media_downloadable import DownloadableMediaMessageProtocolEntity
from yowsup.layers.protocol_media.protocolentities.test_message_media import MediaMessageProtocolEntityTest

class DownloadableMediaMessageProtocolEntityTest(MediaMessageProtocolEntityTest):
    def setUp(self):
        super(DownloadableMediaMessageProtocolEntityTest, self).setUp()
        url = {}
        url["url"] = "URL"
        url["mediaKey"] = "581803027"
        url["file_enc_sha256"] = "95268dd7d020caebde755fcce30ab592204f9684fef2cd97ca0cef87efaa97fd"
        self.ProtocolEntity = DownloadableMediaMessageProtocolEntity
        mediaNode = self.node.getChild("media")
        mediaNode.setAttribute("mimetype",          "MIMETYPE")
        mediaNode.setAttribute("filehash",          "FILEHASH")
        mediaNode.setAttribute("url",               url)
        mediaNode.setAttribute("mediaKey",          url)
        mediaNode.setAttribute("file_enc_sha256",   url)
        mediaNode.setAttribute("ip",                "IP")
        mediaNode.setAttribute("size",              "123")
        mediaNode.setAttribute("file",              "FILE")
