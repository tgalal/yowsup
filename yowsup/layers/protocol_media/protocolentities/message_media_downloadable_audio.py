from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
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
    def __init__(self,
            mimeType, fileHash, url, ip, size, fileName, 
            abitrate, acodec, asampfreq, duration, encoding, origin, seconds, 
            _id = None, _from = None, to = None, notify = None, timestamp = None, 
            participant = None, preview = None, offline = None, retry = None):

        super(AudioDownloadableMediaMessageProtocolEntity, self).__init__("audio",
            mimeType, fileHash, url, ip, size, fileName,
            _id, _from, to, notify, timestamp, participant, preview, offline, retry)
        self.setAudioProps(abitrate, acodec, asampfreq, duration, encoding, origin, seconds)

    def __str__(self):
        out  = super(AudioDownloadableMediaMessageProtocolEntity, self).__str__()
        out += "Bitrate: %s\n" % self.abitrate
        out += "Codec: %s\n" % self.acodec
        out += "Duration: %s\n" % self.duration
        out += "Encoding: %s\n" % self.encoding
        out += "Origin: %s\n" % self.origin
        out += "Sampling freq.: %s\n" % self.asampfreq
        return out

    def setAudioProps(self, abitrate, acodec, asampfreq, duration, encoding, origin, seconds):
        self.abitrate  = abitrate
        self.acodec    = acodec
        self.asampfreq = asampfreq
        self.duration  = duration
        self.encoding  = encoding
        self.origin    = origin
        self.seconds   = seconds

    def toProtocolTreeNode(self):
        node = super(AudioDownloadableMediaMessageProtocolEntity, self).toProtocolTreeNode()
        mediaNode = node.getChild("media")

        mediaNode.setAttribute("abitrate",  self.abitrate)
        mediaNode.setAttribute("acodec",    self.acodec)
        mediaNode.setAttribute("asampfreq", self.asampfreq)
        mediaNode.setAttribute("duration",  self.duration)
        mediaNode.setAttribute("encoding",  self.encoding)
        mediaNode.setAttribute("origin",    self.origin)
        mediaNode.setAttribute("seconds",   self.seconds)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = DownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = AudioDownloadableMediaMessageProtocolEntity
        mediaNode = node.getChild("media")
        entity.setAudioProps(
            mediaNode.getAttributeValue("abitrate"),
            mediaNode.getAttributeValue("acodec"),
            mediaNode.getAttributeValue("asampfreq"),
            mediaNode.getAttributeValue("duration"),
            mediaNode.getAttributeValue("encoding"),
            mediaNode.getAttributeValue("origin"),
            mediaNode.getAttributeValue("seconds"),
        )
        return entity
