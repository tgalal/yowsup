from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
class VideoDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
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
            abitrate, acodec, asampfmt, asampfreq, duration, encoding, fps, height, preview, seconds, vbitrate, vcodec, width, 
            _id = None, _from = None, to = None, notify = None, timestamp = None, 
            participant = None, offline = None, retry = None):

        super(VideoDownloadableMediaMessageProtocolEntity, self).__init__("video",
            mimeType, fileHash, url, ip, size, fileName,
            _id, _from, to, notify, timestamp, participant, offline, retry)
        self.setVideoProps(abitrate, acodec, asampfmt, asampfreq, duration, encoding, fps, height, preview, seconds, vbitrate, vcodec, width)

    def __str__(self):
        out  = super(VideoDownloadableMediaMessageProtocolEntity, self).__str__()
        out += "Audio bitrate: %s\n" % self.abitrate
        out += "Audio codec: %s\n" % self.acodec
        out += "Audio sampling fmt.: %s\n" % self.asampfmt
        out += "Audio sampling freq.: %s\n" % self.asampfreq
        out += "Duration: %s\n" % self.duration
        out += "Encoding: %s\n" % self.encoding
        out += "Fps: %s\n" % self.fps
        out += "Height: %s\n" % self.height
        out += "Video bitrate: %s\n" % self.vbitrate
        out += "Video codec: %s\n" % self.vcodec
        out += "Width: %s\n" % self.width
        return out

    def setVideoProps(self, abitrate, acodec, asampfmt, asampfreq, duration, encoding, fps, height, preview, seconds, vbitrate, vcodec, width):
        self.abitrate  = abitrate
        self.acodec    = acodec
        self.asampfmt  = asampfmt
        self.asampfreq = asampfreq
        self.duration  = duration
        self.encoding  = encoding
        self.fps       = fps
        self.height    = height
        self.preview   = preview
        self.seconds   = seconds
        self.vbitrate  = vbitrate
        self.vcodec    = vcodec
        self.width     = width
        
    def getPreview(self):
        return self.preview

    def toProtocolTreeNode(self):
        node = super(VideoDownloadableMediaMessageProtocolEntity, self).toProtocolTreeNode()
        mediaNode = node.getChild("media")

        mediaNode.setAttribute("abitrate",  self.abitrate)
        mediaNode.setAttribute("acodec",    self.acodec)
        mediaNode.setAttribute("asampfmt",  self.asampfmt)
        mediaNode.setAttribute("asampfreq", self.asampfreq)
        mediaNode.setAttribute("duration",  self.duration)
        mediaNode.setAttribute("encoding",  self.encoding)
        mediaNode.setAttribute("fps",       self.fps)
        mediaNode.setAttribute("height",    self.height)
        mediaNode.setAttribute("seconds",   self.seconds)
        mediaNode.setAttribute("vbitrate",  self.vbitrate)
        mediaNode.setAttribute("vcodec",    self.vcodec)
        mediaNode.setAttribute("width",     self.width)
        
        mediaNode.setData(self.preview)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = DownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = VideoDownloadableMediaMessageProtocolEntity
        mediaNode = node.getChild("media")
        entity.setVideoProps(
            mediaNode.getAttributeValue("abitrate"),
            mediaNode.getAttributeValue("acodec"),
            mediaNode.getAttributeValue("asampfmt"),
            mediaNode.getAttributeValue("asampfreq"),
            mediaNode.getAttributeValue("duration"),
            mediaNode.getAttributeValue("encoding"),
            mediaNode.getAttributeValue("fps"),
            mediaNode.getAttributeValue("height"),
            mediaNode.getData(),
            mediaNode.getAttributeValue("seconds"),
            mediaNode.getAttributeValue("vbitrate"),
            mediaNode.getAttributeValue("vcodec"),
            mediaNode.getAttributeValue("width"),
        )
        return entity
