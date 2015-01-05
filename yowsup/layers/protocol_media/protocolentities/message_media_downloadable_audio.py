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
            mimeType, fileHash, url, ip, size, fileName, encoding, caption = None,
            _id = None, _from = None, to = None, notify = None, timestamp = None, 
            participant = None, offline = None, retry = None):

        super(AudioDownloadableMediaMessageProtocolEntity, self).__init__("audio",
            mimeType, fileHash, url, ip, size, fileName,
            _id, _from, to, notify, timestamp, participant, preview, offline, retry)
        self.setAudioProps(encoding, caption)

    def __str__(self):
        out  = super(AudioDownloadableMediaMessageProtocolEntity, self).__str__()
        out += "Encoding: %s\n" % self.encoding
        return out

    def setAudioProps(self, encoding, caption):
        self.encoding   = encoding
        self.caption    = caption

    def getCaption(self):
        return self.caption

    def toProtocolTreeNode(self):
        node = super(AudioDownloadableMediaMessageProtocolEntity, self).toProtocolTreeNode()
        mediaNode = node.getChild("media")

        mediaNode.setAttribute("encoding",  self.encoding)
        if self.caption:
            mediaNode.setAttribute("caption", self.caption)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = DownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = AudioDownloadableMediaMessageProtocolEntity
        mediaNode = node.getChild("media")
        entity.setAudioProps(
            mediaNode.getAttributeValue("encoding"),
            mediaNode.getAttributeValue("caption")
            )
        return entity
