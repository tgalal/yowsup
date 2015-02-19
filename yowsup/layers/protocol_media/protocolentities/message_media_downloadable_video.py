from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from yowsup.common.tools import VideoTools
import math
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

        <media type="video"
            mimetype="video/mp4"
            filehash="b/f7d5bF7wK7GPqo4kH7qeka/JG0KzkFjUC4Veq9Iwg="
            url="https://mms880.whatsapp.net/d/Y00AgRfYWMWZQXTXgy_FJ1Rfe9YABQdt914Dvg/ArZwkA1pbhHdyC5eXRzgPb-DCK4K7PooUUi0kYGxm-wj.mp4"
            ip="173.193.205.8"
            size="112928"
            file="ArZwkA1pbhHdyC5eXRzgPb-DCK4K7PooUUi0kYGxm-wj.mp4"

            fps="25"
            encoding="raw"
            seconds="1"
            vcodec="h264"
            abitrate="60"
            vbitrate="726"
            height="360"
            asampfmt="flt"
            duration="1"
            asampfreq="44100"
            acodec="aac"
            width="480"
        >{{THUMBNAIL_RAWDATA}}</media>

    </message>
    '''
    def __init__(self,
            mimeType, fileHash, url, ip, size, fileName,
            encoding, width, height, caption = None,
            _id = None, _from = None, to = None, notify = None, timestamp = None, participant = None,
            preview = None, offline = None, retry = None, vcodec = None, abitrate = None, vbitrate = None,
            seconds = None, asampfmt = None, duration = None, asampfreq = None, acodec = None):

        super(VideoDownloadableMediaMessageProtocolEntity, self).__init__("video",
            mimeType, fileHash, url, ip, size, fileName,
            _id, _from, to, notify, timestamp, participant, preview, offline, retry)
        self.setVideoProps(encoding, width, height, caption, vcodec, abitrate, vbitrate, seconds, asampfmt, duration, asampfreq, acodec)

    def __str__(self):
        out  = super(VideoDownloadableMediaMessageProtocolEntity, self).__str__()
        out += "Encoding: %s\n" % self.encoding
        out += "Width: %s\n" % self.width
        out += "Height: %s\n" % self.height
        return out

    def setVideoProps(self, encoding, width, height, caption, vcodec, abitrate, vbitrate, seconds, asampfmt, duration, asampfreq, acodec):
        self.encoding   = encoding
        self.width      = int(width)
        self.height     = int(height)
        self.caption    = caption
        self.vcodec     = vcodec
        self.abitrate   = abitrate
        self.vbitrate   = vbitrate
        self.seconds    = seconds
        self.asampfmt   = asampfmt
        self.duration   = duration
        self.asampfreq  = asampfreq
        self.acodec     = acodec

    def getCaption(self):
        return self.caption

    def toProtocolTreeNode(self):
        node = super(VideoDownloadableMediaMessageProtocolEntity, self).toProtocolTreeNode()
        mediaNode = node.getChild("media")

        mediaNode.setAttribute("encoding",  self.encoding)
        mediaNode.setAttribute("width",     str(self.width))
        mediaNode.setAttribute("height",    str(self.height))
        if self.caption:
            mediaNode.setAttribute("caption", self.caption)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = DownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = VideoDownloadableMediaMessageProtocolEntity
        mediaNode = node.getChild("media")
        entity.setVideoProps(
            mediaNode.getAttributeValue("encoding"),
            mediaNode.getAttributeValue("width"),
            mediaNode.getAttributeValue("height"),
            mediaNode.getAttributeValue("caption"),
            mediaNode.getAttributeValue("vcodec"),
            mediaNode.getAttributeValue("abitrate"),
            mediaNode.getAttributeValue("vbitrate"),
            mediaNode.getAttributeValue("seconds"),
            mediaNode.getAttributeValue("asampfmt"),
            mediaNode.getAttributeValue("duration"),
            mediaNode.getAttributeValue("asampfreq"),
            mediaNode.getAttributeValue("acodec")
            )
        return entity


    @staticmethod
    def fromFilePath(path, url, ip, to, mimeType = None, caption = None, dimensions = None):
        preview = VideoTools.generatePreviewFromVideo(path)
        entity = DownloadableMediaMessageProtocolEntity.fromFilePath(path, url, DownloadableMediaMessageProtocolEntity.MEDIA_TYPE_VIDEO, ip, to, mimeType, preview)
        entity.__class__ = VideoDownloadableMediaMessageProtocolEntity

        if not dimensions:
            format = VideoTools.getVideoFormat(path)

        assert format, "Could not determine video format info"

        width = format['streams'][0]['width']
        height = format['streams'][0]['height']
        vcodec =format['streams'][0]['codec_name']
        abitrate= int(float(format['streams'][1]['bit_rate']))
        vbitrate= int(float(format['streams'][0]['bit_rate']))
        seconds= int(float(format['format']['duration']))
        asampfmt='flt'
        duration= math.floor(float(format['format']['duration']))
        asampfreq=int(float(format['streams'][1]['sample_rate']))
        acodec=format['streams'][1]['codec_name']

        entity.setVideoProps("raw", width, height, caption, vcodec, abitrate, vbitrate, seconds, asampfmt, duration, asampfreq, acodec)
        return entity

