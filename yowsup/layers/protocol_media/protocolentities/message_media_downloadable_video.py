from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from yowsup.common.tools import VideoTools, MimeTools
from Crypto.Cipher import AES
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from axolotl.kdf.hkdfv3 import HKDFv3
from axolotl.util.byteutil import ByteUtil
import binascii
import base64


class VideoDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
    '''
    <message t="{{TIME_STAMP}}" from="{{CONTACT_JID}}" 
        offline="{{OFFLINE}}" type="media" id="{{MESSAGE_ID}}" notify="{{NOTIFY_NAME}}">
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

            origin="forward"           
            > {{THUMBNAIL_RAWDATA (JPEG?)}}
        </media>
    </message>
    '''
    cryptKeys = ''

    def __init__(self,
                 mimeType, fileHash, url, ip, size, fileName,
                 abitrate, acodec, asampfmt, asampfreq, duration, encoding, fps,
                 width, height, seconds, vbitrate, vcodec, caption=None, mediaKey = None,
                 _id=None, _from=None, to=None, notify=None, timestamp=None,
                 participant=None, preview=None, offline=None, retry=None):

        super(VideoDownloadableMediaMessageProtocolEntity, self).__init__("video",
                                                                          mimeType, fileHash, url, ip, size, fileName, mediaKey,
                                                                          None, _id, _from, to, notify, timestamp,
                                                                          participant, preview, offline, retry)
        self.setVideoProps(encoding, width, height, vbitrate, abitrate, acodec, asampfmt, asampfreq, duration, fps,
                           seconds, vcodec, caption)
        cryptKeys = '576861747341707020566964656f204b657973'

    def __str__(self):
        out = super(VideoDownloadableMediaMessageProtocolEntity, self).__str__()
        out += "Audio bitrate: %s\n" % self.abitrate
        out += "Audio codec: %s\n" % self.acodec
        out += "Audio sampling fmt.: %s\n" % self.asampfmt
        out += "Audio sampling freq.: %s\n" % self.asampfreq
        out += "Duration: %s\n" % self.duration
        out += "Encoding: %s\n" % self.encoding
        out += "Fps: %s\n" % self.fps
        out += "Width: %s\n" % self.width
        out += "Height: %s\n" % self.height
        out += "Video bitrate: %s\n" % self.vbitrate
        out += "Video codec: %s\n" % self.vcodec
        if self.caption is not None:
            out += "Caption: %s\n" % self.caption
        return out

    def setVideoProps(self, encoding, width, height, vbitrate=None, abitrate=None, acodec=None, asampfmt=None,
                      asampfreq=None, duration=None, fps=None, seconds=None, vcodec=None, caption=None, ):
        self.abitrate  = abitrate
        self.acodec    = acodec
        self.asampfmt  = asampfmt
        self.asampfreq = asampfreq
        self.duration  = duration
        self.encoding  = encoding
        self.fps       = fps
        self.height    = height
        self.seconds   = seconds
        self.vbitrate  = vbitrate
        self.vcodec    = vcodec
        self.width     = width
        self.caption   = caption
        self.cryptKeys = '576861747341707020566964656f204b657973'

    def setMimeType(self, mimeType):
        self.mimeType = mimeType

    def getExtension(self):
        return MimeTools.getExtension(self.mimeType)

    def getCaption(self):
        return self.caption

    def toProtocolTreeNode(self):
        node = super(VideoDownloadableMediaMessageProtocolEntity, self).toProtocolTreeNode()
        mediaNode = node.getChild("enc")
        if self.abitrate is not None:
            mediaNode.setAttribute("abitrate", self.abitrate)
        if self.acodec is not None:
            mediaNode.setAttribute("acodec", self.acodec)
        if self.asampfmt is not None:
            mediaNode.setAttribute("asampfmt", self.asampfmt)
        if self.asampfreq is not None:
            mediaNode.setAttribute("asampfreq", self.asampfreq)
        if self.duration is not None:
            mediaNode.setAttribute("duration", self.duration)
        if self.encoding is not None:
            mediaNode.setAttribute("encoding", self.encoding)
        mediaNode.setAttribute("height", str(self.height))
        mediaNode.setAttribute("width", str(self.width))
        if self.abitrate is not None:
            mediaNode.setAttribute("abitrate", str(self.abitrate))
        if self.acodec is not None:
            mediaNode.setAttribute("acodec", self.acodec)
        if self.asampfmt is not None:
            mediaNode.setAttribute("asampfmt", self.asampfmt)
        if self.asampfreq is not None:
            mediaNode.setAttribute("asampfreq", str(self.asampfreq))
        if self.duration is not None:
            mediaNode.setAttribute("duration", str(self.duration))
        if self.fps is not None:
            mediaNode.setAttribute("fps", str(self.fps))
        if self.seconds is not None:
            mediaNode.setAttribute("seconds", str(self.seconds))
        if self.vbitrate is not None:
            mediaNode.setAttribute("vbitrate", str(self.vbitrate))
        if self.vcodec is not None:
            mediaNode.setAttribute("vcodec", self.vcodec)
        if self.caption is not None:
            mediaNode.setAttribute("caption", self.caption)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = DownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = VideoDownloadableMediaMessageProtocolEntity
        mediaNode = node.getChild("media")
        entity.setMimeType(mediaNode.getAttributeValue("mimetype"))
        entity.setVideoProps(
            mediaNode.getAttributeValue("encoding"),
            mediaNode.getAttributeValue("width"),
            mediaNode.getAttributeValue("height"),
            mediaNode.getAttributeValue("vbitrate"),
            mediaNode.getAttributeValue("abitrate"),
            mediaNode.getAttributeValue("acodec"),
            mediaNode.getAttributeValue("asampfmt"),
            mediaNode.getAttributeValue("asampfreq"),
            mediaNode.getAttributeValue("duration"),
            mediaNode.getAttributeValue("fps"),
            mediaNode.getAttributeValue("seconds"),
            mediaNode.getAttributeValue("vcodec"),
            mediaNode.getAttributeValue("caption")
        )
        return entity

    @staticmethod
    def fromFilePath(path, url, ip, to, mimeType=None, caption=None):
        preview = VideoTools.generatePreviewFromVideo(path)
        entity = DownloadableMediaMessageProtocolEntity.fromFilePath(path, url,
                                                                     DownloadableMediaMessageProtocolEntity.MEDIA_TYPE_VIDEO,
                                                                     ip, to, mimeType, preview)
        entity.__class__ = VideoDownloadableMediaMessageProtocolEntity

        width, height, bitrate, duration = VideoTools.getVideoProperties(path)
        assert width, "Could not determine video properties"

        duration = int(duration)
        entity.setVideoProps('raw', width, height, duration=duration, seconds=duration, caption=caption)
        return entity


    def decrypt(self, encvid, refkey):
        derivative = HKDFv3().deriveSecrets(refkey, binascii.unhexlify(self.cryptKeys), 112)
        parts = ByteUtil.split(derivative, 16, 32)
        iv = parts[0]
        cipherKey = parts[1]
        e_vid = encvid[:-10]
        AES.key_size = 128
        cr_obj = AES.new(key=cipherKey, mode=AES.MODE_CBC, IV=iv)
        return cr_obj.decrypt(e_vid)


    def isEncrypted(self):
        return self.cryptKeys and self.mediaKey


    def getMediaContent(self):
        data = urlopen(self.url.decode('ASCII')).read()
        # data = urlopen(self.url).read()
        if self.isEncrypted():
            data = self.decrypt(data, self.mediaKey)
        return bytearray(data)