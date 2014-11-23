from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
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
            mediaType, mimeType, fileHash, url, ip, size, fileName,
            encoding, width, height,
            _id = None, _from = None, to = None, notify = None, timestamp = None, participant = None,
            preview = None, offline = None, retry = None):

        super(MediaMessageProtocolEntity, self).__init__(mediaType, 
            _id, _from, to, notify, timestamp, participant, preview, offline, retry)
        self.setImageProps(encoding, width, height)
        self.setDownloadableMediaProps(mimeType, fileHash, url, ip, size, fileName)

    def __str__(self):
        out  = super(ImageDownloadableMediaMessageProtocolEntity, self).__str__()
        out += "Encoding: %s\n" % self.encoding
        out += "Width: %s\n" % self.width
        out += "Height: %s\n" % self.height
        return out

    def setImageProps(self, encoding, width, height):
        self.encoding   = encoding
        self.width      = int(width)
        self.height     = int(height)

    def toProtocolTreeNode(self):
        node = super(DownloadableMediaMessageProtocolEntity, self).toProtocolTreeNode()
        mediaNode = node.getChild("media")

        mediaNode.setAttribute("encoding",  self.encoding)
        mediaNode.setAttribute("width",     str(self.width))
        mediaNode.setAttribute("height",    str(self.height))

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = DownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = ImageDownloadableMediaMessageProtocolEntity
        mediaNode = node.getChild("media")
        entity.setImageProps(
            mediaNode.getAttributeValue("encoding"),
            mediaNode.getAttributeValue("width"),
            mediaNode.getAttributeValue("height")
            )
        return entity
