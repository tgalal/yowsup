from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from Crypto.Cipher import AES
try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen
from yowsup.common.tools import AudioTools, MimeTools
from axolotl.kdf.hkdfv3 import HKDFv3
from axolotl.util.byteutil import ByteUtil
import binascii
import base64
class AudioDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
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
    cryptKeys = ''

    def __init__(self,
            mimeType, fileHash, url, ip, size, fileName,
            abitrate, acodec, asampfreq, duration, encoding, origin, seconds, mediaKey = None,
            _id = None, _from = None, to = None, notify = None, timestamp = None,
            participant = None, preview = None, offline = None, retry = None):

        super(AudioDownloadableMediaMessageProtocolEntity, self).__init__("audio",
            mimeType, fileHash, url, ip, size, fileName, mediaKey, None,
            _id, _from, to, notify, timestamp, participant, preview, offline, retry)
        self.setAudioProps(abitrate, acodec, asampfreq, duration, encoding, origin, seconds)
        self.cryptKeys = '576861747341707020417564696f204b657973'

    def __str__(self):
        out  = super(AudioDownloadableMediaMessageProtocolEntity, self).__str__()
        out += "mimeType: %s\n" % self.mimeType
        out += "Duration: %s\n" % self.duration
        return out

    def setMimeType(self, mimeType):
        self.mimeType = mimeType

    def getExtension(self):
        return MimeTools.getExtension(self.mimeType)

    def setAudioProps(self, duration = None):
        self.duration  = duration
        self.cryptKeys = '576861747341707020417564696f204b657973'

    def toProtocolTreeNode(self):
        node = super(AudioDownloadableMediaMessageProtocolEntity, self).toProtocolTreeNode()
        mediaNode = node.getChild("enc")
        mediaNode.setAttribute("duration",  self.duration)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = DownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = AudioDownloadableMediaMessageProtocolEntity
        mediaNode = node.getChild("media")
        entity.setMimeType(mediaNode.getAttributeValue("mimetype"))
        entity.setAudioProps(
            mediaNode.getAttributeValue("duration")
        )
        return entity



    @staticmethod
    def fromFilePath(fpath, url, ip, to, mimeType = None, preview = None, filehash = None, filesize = None):
        entity = DownloadableMediaMessageProtocolEntity.fromFilePath(fpath, url, DownloadableMediaMessageProtocolEntity.MEDIA_TYPE_AUDIO, ip, to, mimeType, preview)
        entity.__class__ = AudioDownloadableMediaMessageProtocolEntity
        duration = AudioTools.getAudioProperties(fpath)
        entity.setAudioProps(duration=duration)

        return entity


    def decrypt(self, encaud, refkey):
        derivative = HKDFv3().deriveSecrets(refkey, binascii.unhexlify(self.cryptKeys), 112)
        parts = ByteUtil.split(derivative, 16, 32)
        iv = parts[0]
        cipherKey = parts[1]
        e_aud = encaud[:-10]
        AES.key_size = 128
        cr_obj = AES.new(key=cipherKey, mode=AES.MODE_CBC, IV=iv)
        return cr_obj.decrypt(e_aud)


    def isEncrypted(self):
        return self.cryptKeys and self.mediaKey


    def getMediaContent(self):
        data = urlopen(self.url.decode('ASCII')).read()
        # data = urlopen(self.url).read()
        if self.isEncrypted():
            data = self.decrypt(data, self.mediaKey)
        return bytearray(data)