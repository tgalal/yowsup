from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message_media import MediaMessageProtocolEntity
class DownloadableMediaMessageProtocolEntity(MediaMessageProtocolEntity):
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

            > {{THUMBNAIL_RAWDATA (JPEG?)}}
        </media>
    </message>
    '''
    def __init__(self, _id, _from, mediaType, mimeType, fileHash, url, ip, size, fileName, timestamp, notify, preview = None, offline = False, retry = None):
        super(MediaMessageProtocolEntity, self).__init__(_id, _from, mediaType, timestamp, notify, preview, offline, retry)
        self.setDownloadableMediaProps(mimeType, fileHash, url, ip, size, fileName)

    def setDownloadableMediaProps(self, mimeType, fileHash, url, ip, size, fileName):
        self.mimeType   = mimeType
        self.fileHash   = fileHash
        self.url        = url
        self.ip         = ip
        self.size       = int(size)
        self.fileName   = fileName

    def toProtocolTreeNode(self):
        node = super(DownloadableMediaMessageProtocolEntity, self).toProtocolTreeNode()
        mediaNode = node.getChild("media")
        mediaNode.setAttribute("mimetype",  self.mimeType)
        mediaNode.setAttribute("filehash",  self.fileHash)
        mediaNode.setAttribute("url",       self.url)
        mediaNode.setAttribute("ip",        self.ip)
        mediaNode.setAttribute("size",      str(self.size))
        mediaNode.setAttribute("file",      self.fileName)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = MediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = DownloadableMediaMessageProtocolEntity
        entity.setDownloadableMediaProps(
            node.getAtttributeValue("mimetype"),
            node.getAtttributeValue("filehash"),
            node.getAtttributeValue("url"),
            node.getAtttributeValue("ip"),
            node.getAtttributeValue("size"),
            node.getAtttributeValue("file")
            )
        return entity
