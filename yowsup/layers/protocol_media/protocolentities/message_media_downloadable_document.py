from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from .builder_message_media_downloadable import DownloadableMediaMessageBuilder
from yowsup.layers.protocol_messages.proto.wa_pb2 import DocumentMessage
from yowsup.common.tools import DocumentTools, MimeTools
from Crypto.Cipher import AES
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from axolotl.kdf.hkdfv3 import HKDFv3
from axolotl.util.byteutil import ByteUtil
import binascii
import base64

class DocumentDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
    '''
    <message t="{{TIME_STAMP}}" from="{{CONTACT_JID}}"
        offline="{{OFFLINE}}" type="text" id="{{MESSAGE_ID}}" notify="{{NOTIFY_NAME}}">
        <media type="{{DOWNLOADABLE_MEDIA_TYPE: (image | audio | video | document)}}"
            mimetype="{{MIME_TYPE}}"
            filehash="{{FILE_HASH}}"
            url="{{DOWNLOAD_URL}}"
            ip="{{IP}}"
            size="{{MEDIA SIZE}}"
            file="{{FILENAME}}"


            encoding="{{ENCODING}}"
            height="{{IMAGE_HEIGHT}}"
            width="{{IMAGE_WIDTH}}"

            > {{THUMBNAIL_RAWDATA (JPEG?)}}
        </media>
    </message>
    '''
    DOCUMENT_KEY = "576861747341707020446f63756d656e74204b657973"

    def __init__(self,
            mimeType, fileHash, url, ip, size, fileName, pageCount,
            encoding = None, width = None, height = None, caption = None, mediaKey = None,
            _id = None, _from = None, to = None, notify = None, timestamp = None,
            participant = None, preview = None, offline = None, retry = None):

        super(DocumentDownloadableMediaMessageProtocolEntity, self).__init__("document",
            mimeType, fileHash, url, ip, size, fileName, pageCount, mediaKey,
            _id, _from, to, notify, timestamp, participant, preview, offline, retry)
        print("ENCONDING")
        print(encoding)
        self.setDocumentProps(pageCount)

    def __str__(self):
        out  = super(DocumentDownloadableMediaMessageProtocolEntity, self).__str__()
        out += "Encoding: %s\n" % self.encoding
        #out += "Width: %s\n" % self.width
        #out += "Height: %s\n" % self.height
        if self.caption:
            out += "Caption: %s\n" % self.caption
        return out

    def setDocumentProps(self, pageCount):
        self.pageCount  = str(pageCount)
        self.cryptKeys  = '576861747341707020446f63756d656e74204b657973'

    def setFileName(self, fileName):
        self.fileName = fileName

    def getFileName(self):
        return self.fileName

    def getCaption(self):
        return self.caption

    def toProtocolTreeNode(self):
        node = super(DocumentDownloadableMediaMessageProtocolEntity, self).toProtocolTreeNode()
        mediaNode = node.getChild("enc")
        mediaNode.setAttribute("pageCount", str(self.pageCount))
        return node

    def toProtobufMessage(self):
        document_message = DocumentMessage()
        document_message.url = self.url
        document_message.mime_type = self.mimeType #"application/pdf"
        document_message.title = self.fileName
        document_message.file_sha256 = self.fileHash
        document_message.file_length = self.size
        document_message.page_count = self.pageCount;
        document_message.media_key = self.mediaKey
        document_message.jpeg_thumbnail = self.preview

        print(document_message)
        return document_message

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = DownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = DocumentDownloadableMediaMessageProtocolEntity
        mediaNode = node.getChild("media")
        entity.setFileName(mediaNode.getAttributeValue("title"))
        entity.setDocumentProps(
            mediaNode.getAttributeValue("encoding")
        )
        return entity


    @staticmethod
    def getBuilder(jid, filepath):
        return DownloadableMediaMessageBuilder(DocumentDownloadableMediaMessageProtocolEntity, jid, filepath)

    @staticmethod
    def fromBuilder(builder):
        builder.getOrSet("preview", lambda: DocumentTools.generatePreviewFromDocument(builder.getOriginalFilepath()))
        pageCount = DocumentTools.getDocumentProperties(builder.getOriginalFilepath())
        entity = DownloadableMediaMessageProtocolEntity.fromBuilder(builder)
        entity.__class__ = builder.cls
        entity.setDocumentProps(pageCount)
        return entity

    @staticmethod
    def fromFilePath(path, url, ip, to, mimeType = None):
        print("FROM FILE PATH")
        builder = DocumentDownloadableMediaMessageProtocolEntity.getBuilder(to, path)
        builder.set("url", url)
        builder.set("ip", ip)
        builder.set("mimetype", mimeType)
        return DocumentDownloadableMediaMessageProtocolEntity.fromBuilder(builder)

    def unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]

    def decrypt(self, encdoc, refkey):

        print("REF KEY")
        print(refkey)
        derivative = HKDFv3().deriveSecrets(refkey,
                                            binascii.unhexlify(self.cryptKeys), 112)

        parts = ByteUtil.split(derivative, 16, 32)
        iv = parts[0]
        cipherKey = parts[1]
        e_doc = encdoc[:-10]
        AES.key_size = 128
        cr_obj = AES.new(key=cipherKey, mode=AES.MODE_CBC, IV=iv)
        return cr_obj.decrypt(e_doc)

    def isEncrypted(self):
        return self.cryptKeys and self.mediaKey

    def getMediaContent(self):
        data = urlopen(self.url.decode('ASCII')).read()
        if self.isEncrypted():
            data = self.decrypt(data, self.mediaKey)
        return data

