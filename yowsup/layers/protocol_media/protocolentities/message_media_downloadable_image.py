from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from .builder_message_media_downloadable import DownloadableMediaMessageBuilder
from yowsup.layers.protocol_messages.proto.wa_pb2 import ImageMessage
from yowsup.common.tools import ImageTools, MimeTools
from Crypto.Cipher import AES
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from axolotl.kdf.hkdfv3 import HKDFv3
from axolotl.util.byteutil import ByteUtil
import binascii
import base64

class ImageDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
    '''
    <message t="{{TIME_STAMP}}" from="{{CONTACT_JID}}"
        offline="{{OFFLINE}}" type="text" id="{{MESSAGE_ID}}" notify="{{NOTIFY_NAME}}">
        <media type="{{DOWNLOADABLE_MEDIA_TYPE: (image | audio | video)}}"
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
    def __init__(self,
            mimeType, fileHash, url, ip, size, fileName,
            encoding, width, height, caption = None, mediaKey = None,
            _id = None, _from = None, to = None, notify = None, timestamp = None,
            participant = None, preview = None, offline = None, retry = None):

        super(ImageDownloadableMediaMessageProtocolEntity, self).__init__("image",
            mimeType, fileHash, url, ip, size, fileName, mediaKey,
            _id, _from, to, notify, timestamp, participant, preview, offline, retry)
        self.setImageProps(encoding, width, height, caption)

    def __str__(self):
        out  = super(ImageDownloadableMediaMessageProtocolEntity, self).__str__()
        out += "Encoding: %s\n" % self.encoding
        out += "Width: %s\n" % self.width
        out += "Height: %s\n" % self.height
        if self.caption:
            out += "Caption: %s\n" % self.caption
        return out

    def setImageProps(self, encoding, width, height, caption):
        self.encoding   = encoding
        self.width      = int(width)
        self.height     = int(height)
        self.caption    = caption
        self.cryptKeys = '576861747341707020496d616765204b657973'

    def setMimeType(self, mimeType):
        self.mimeType = mimeType

    def getExtension(self):
        return MimeTools.getExtension(self.mimeType)

    def getCaption(self):
        return self.caption

    def toProtocolTreeNode(self):
        node = super(ImageDownloadableMediaMessageProtocolEntity, self).toProtocolTreeNode()
        mediaNode = node.getChild("enc")

        mediaNode.setAttribute("encoding",  self.encoding)
        mediaNode.setAttribute("width",     str(self.width))
        mediaNode.setAttribute("height",    str(self.height))
        if self.caption:
            mediaNode.setAttribute("caption", self.caption)

        return node

    def toProtobufMessage(self):
        image_message = ImageMessage()
        image_message.url = self.url
        image_message.width = self.width
        image_message.height = self.height
        image_message.mime_type = self.mimeType
        image_message.file_sha256 = self.fileHash
        image_message.file_length = self.size
        image_message.caption = self.caption
        image_message.jpeg_thumbnail = self.preview
        image_message.media_key = self.mediaKey

        return image_message

    @staticmethod
    def fromProtocolTreeNode(node):

        entity = DownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = ImageDownloadableMediaMessageProtocolEntity
        mediaNode = node.getChild("media")
        entity.setMimeType(mediaNode.getAttributeValue("mimetype"))
        entity.setImageProps(
            mediaNode.getAttributeValue("encoding"),
            mediaNode.getAttributeValue("width"),
            mediaNode.getAttributeValue("height"),
            mediaNode.getAttributeValue("caption")
        )
        return entity


    @staticmethod
    def getBuilder(jid, filepath):
        return DownloadableMediaMessageBuilder(ImageDownloadableMediaMessageProtocolEntity, jid, filepath)

    @staticmethod
    def fromBuilder(builder):
        builder.getOrSet("preview", lambda: ImageTools.generatePreviewFromImage(builder.getOriginalFilepath()))
        filepath = builder.getFilepath()
        caption = builder.get("caption")
        mimeType = builder.get("mimetype")
        dimensions = builder.get("dimensions",  ImageTools.getImageDimensions(builder.getOriginalFilepath()))
        assert dimensions, "Could not determine image dimensions"
        width, height = dimensions

        entity = DownloadableMediaMessageProtocolEntity.fromBuilder(builder)
        entity.__class__ = builder.cls
        entity.setImageProps("raw", width, height, caption)
        return entity

    @staticmethod
    def fromFilePath(path, url, ip, to, mimeType = None, caption = None, dimensions = None):
        builder = ImageDownloadableMediaMessageProtocolEntity.getBuilder(to, path)
        builder.set("url", url)
        builder.set("ip", ip)
        builder.set("caption", caption)
        builder.set("mimetype", mimeType)
        builder.set("dimensions", dimensions)
        return ImageDownloadableMediaMessageProtocolEntity.fromBuilder(builder)


    def decrypt(self, encimg, refkey):
        derivative = HKDFv3().deriveSecrets(refkey, binascii.unhexlify(self.cryptKeys), 112)
        parts = ByteUtil.split(derivative, 16, 32)
        iv = parts[0]
        cipherKey = parts[1]
        e_img = encimg[:-10]
        AES.key_size = 128
        cr_obj = AES.new(key=cipherKey, mode=AES.MODE_CBC, IV=iv)
        return cr_obj.decrypt(e_img)

    def isEncrypted(self):
        return self.cryptKeys and self.mediaKey


    def getMediaContent(self):
        data = urlopen(self.url.decode('ASCII')).read()
        #data = urlopen(self.url).read()
        if self.isEncrypted():
            data = self.decrypt(data, self.mediaKey)
        return bytearray(data)