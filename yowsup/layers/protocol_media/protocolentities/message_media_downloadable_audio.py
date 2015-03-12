from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from yowsup.common.tools import AudioTools
import math
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


            origin="live"
            seconds="1"
            abitrate="32"
            duration="1"
            asampfreq="22050"
            acodec="aac"
            
            > {{THUMBNAIL_RAWDATA (JPEG?)}}
        </media>


        <media type="audio"

            mimetype="audio/aac"
            filehash="86nonv++wq864nlkmbhJXZyPbILLlQ2KyYZxsLo8z1g="
            url="https://mms884.whatsapp.net/d/h72eS2EAV6YrHfZLBaqzFVRffGUABQdt_-pVhg/Arlt8j7XkRsfFw22i-KRffXxl7j9iVsYLbJN4APwsKGJ.aac"
            ip="174.37.199.214"
            size="6003"
            file="Arlt8j7XkRsfFw22i-KRffXxl7j9iVsYLbJN4APwsKGJ.aac"


            origin="live"
            seconds="1"
            abitrate="32"
            duration="1"
            asampfreq="22050"
            acodec="aac"
        ></media>


    </message>
    '''
    def __init__(self,
            mimeType, fileHash, url, ip, size, fileName,
            _id = None, _from = None, to = None, notify = None, timestamp = None, participant = None,
            preview = None, offline = None, retry = None, abitrate = None,
            seconds = None, duration = None, asampfreq = None, acodec = None, origin=None):

        super(AudioDownloadableMediaMessageProtocolEntity, self).__init__("audio",
            mimeType, fileHash, url, ip, size, fileName,
            _id, _from, to, notify, timestamp, participant, preview, offline, retry)
        self.setAudioProps(abitrate, seconds, duration, asampfreq, acodec, origin)

    def __str__(self):
        out  = super(VideoDownloadableMediaMessageProtocolEntity, self).__str__()
        out += "Encoding: %s\n" % self.encoding
        out += "Width: %s\n" % self.width
        out += "Height: %s\n" % self.height
        return out

    def setAudioProps(self, abitrate, seconds, duration, asampfreq, acodec, origin):
        self.abitrate   = abitrate
        self.seconds    = seconds
        self.duration   = duration
        self.asampfreq  = asampfreq
        self.acodec     = acodec
        self.origin     = origin


    def toProtocolTreeNode(self):
        node = super(AudioDownloadableMediaMessageProtocolEntity, self).toProtocolTreeNode()
        mediaNode = node.getChild("media")

        mediaNode.setAttribute("abitrate",  str(self.abitrate))
        mediaNode.setAttribute("seconds",  str(self.seconds))
        mediaNode.setAttribute("duration",  str(self.duration))
        mediaNode.setAttribute("asampfreq",  str(self.asampfreq))
        mediaNode.setAttribute("acodec",  self.acodec)
        mediaNode.setAttribute("origin",  self.origin)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = DownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = AudioDownloadableMediaMessageProtocolEntity
        mediaNode = node.getChild("media")
        entity.setAudioProps(
            mediaNode.getAttributeValue("abitrate"),
            mediaNode.getAttributeValue("seconds"),
            mediaNode.getAttributeValue("duration"),
            mediaNode.getAttributeValue("asampfreq"),
            mediaNode.getAttributeValue("acodec"),
            mediaNode.getAttributeValue("origin")
            )
        return entity


    @staticmethod
    def fromFilePath(path, url, ip, to, mimeType = None):
        entity = DownloadableMediaMessageProtocolEntity.fromFilePath(path, url, DownloadableMediaMessageProtocolEntity.MEDIA_TYPE_AUDIO, ip, to, mimeType)
        entity.__class__ = AudioDownloadableMediaMessageProtocolEntity

        format = AudioTools.getAudioFormat(path)

        assert format, "Could not determine video format info"

        abitrate= int(float(format['streams'][0]['bit_rate']))
        seconds= int(float(format['format']['duration']))
        duration= math.floor(float(format['format']['duration']))
        asampfreq=int(float(format['streams'][0]['sample_rate']))
        acodec=format['streams'][0]['codec_name']
        origin="live"

        entity.setAudioProps(abitrate, seconds, duration, asampfreq, acodec, origin)
        return entity

