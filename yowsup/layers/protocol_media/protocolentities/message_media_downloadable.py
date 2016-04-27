from .message_media import MediaMessageProtocolEntity
from yowsup.common.tools import WATools
from yowsup.common.tools import MimeTools
import os
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
    def __init__(self, mediaType,
            mimeType, fileHash, url, ip, size, fileName, 
            _id = None, _from = None, to = None, notify = None, timestamp = None, 
            participant = None, preview = None, offline = None, retry = None):

        super(DownloadableMediaMessageProtocolEntity, self).__init__(mediaType, _id, _from, to, notify, timestamp, participant, preview, offline, retry)
        self.setDownloadableMediaProps(mimeType, fileHash, url, ip, size, fileName)

    def __str__(self):
        out  = super(DownloadableMediaMessageProtocolEntity, self).__str__()
        out += "MimeType: %s\n" % self.mimeType
        out += "File Hash: %s\n" % self.fileHash.encode('hex')
        out += "URL: %s\n" % self.url
        out += "IP: %s\n" % self.ip
        out += "File Size: %s\n" % self.size
        out += "File name: %s\n" % self.fileName
        return out

    def getMediaSize(self):
        return self.size

    def getMediaUrl(self):
        return self.url

    def getMimeType(self):
        return self.mimeType

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
        if self.ip:
            mediaNode.setAttribute("ip",        self.ip)
        mediaNode.setAttribute("size",      str(self.size))
        mediaNode.setAttribute("file",      self.fileName)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = MediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = DownloadableMediaMessageProtocolEntity
        mediaNode = node.getChild("media")
        entity.setDownloadableMediaProps(
            mediaNode.getAttributeValue("mimetype"),
            mediaNode.getAttributeValue("filehash"),
            mediaNode.getAttributeValue("url"),
            mediaNode.getAttributeValue("ip"),
            mediaNode.getAttributeValue("size"),
            mediaNode.getAttributeValue("file")
            )
        return entity

    @staticmethod
    def fromFilePath(fpath, url, mediaType, ip, to, mimeType = None, preview = None, filehash = None, filesize = None):
        mimeType = mimeType or MimeTools.getMIME(fpath)
        filehash = filehash or WATools.getFileHashForUpload(fpath)
        size = filesize or os.path.getsize(fpath)
        fileName = os.path.basename(fpath)

        return DownloadableMediaMessageProtocolEntity(mediaType, mimeType, filehash, url, ip, size, fileName, to = to, preview = preview)


