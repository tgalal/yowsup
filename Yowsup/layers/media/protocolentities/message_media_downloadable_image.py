from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
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
    def __init__(self, _id, _from,
            mediaType, mimeType, fileHash, url, ip, size, fileName,
            encoding, width, height,
            timestamp, notify,
            preview = None, offline = False, retry = None):

        super(MediaMessageProtocolEntity, self).__init__(_id, _from, mediaType, timestamp, notify, preview, offline, retry)
        self.setImageProps(encoding, width, height)
        self.setDownloadableMediaProps(mimeType, fileHash, url, ip, size, fileName)

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
        entity.setImageProps(
            node.getAtttributeValue("encoding"),
            node.getAtttributeValue("width"),
            node.getAtttributeValue("height")
            )
        return entity
