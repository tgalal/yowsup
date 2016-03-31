from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message_media_downloadable import DownloadableMediaMessageProtocolEntity
from .builder_message_media_downloadable import DownloadableMediaMessageBuilder
from yowsup.layers.protocol_messages.proto.wa_pb2 import ImageMessage
from yowsup.common.tools import ImageTools

class DocumentDownloadableMediaMessageProtocolEntity(DownloadableMediaMessageProtocolEntity):
    '''
    <message t="{{TIME_STAMP}}" from="{{CONTACT_JID}}"
        offline="{{OFFLINE}}" type="text" id="{{MESSAGE_ID}}" notify="{{NOTIFY_NAME}}">
        <media type="{{DOWNLOADABLE_MEDIA_TYPE: (image | audio | video)}}"
            mimetype="{{MIME_TYPE}}"
            filehash="{{FILE_HASH}}"
            url="{{DOWNLOAD_URL}}"
            title="{{TITLE}}"
            size="{{MEDIA SIZE}}"
            file="{{FILENAME}}"
            pages="{{PAGE_COUNT}}"


            mediakey="{{MEDIAKEY}}"

            > {{THUMBNAIL_RAWDATA (JPEG?)}}
        </media>
    </message>
    '''
    def __init__(self,
            mimeType, fileHash, url, title, size, fileName,
            pages, mediaKey = None,
            _id = None, _from = None, to = None, notify = None, timestamp = None,
            participant = None, preview = None, offline = None, retry = None):

        super(DocumentDownloadableMediaMessageProtocolEntity, self).__init__("document",
            mimeType, fileHash, url, None, size, fileName, mediaKey,
            _id, _from, to, notify, timestamp, participant, preview, offline, retry)
        self.setImageProps(title, pages)

    def __str__(self):
        out  = super(DocumentDownloadableMediaMessageProtocolEntity, self).__str__()
        out += "Title: %s\n" % self.title
        out += "Pages: %s\n" % str(self.pages)
        return out

    def setDocumentProps(self, title, pages):
        self.pages      = int(pages)
        self.title      = title
        self.cryptKeys  = '576861747341707020446f63756d656e74204b657973'

    def getTitle(self):
        return self.title

    def toProtocolTreeNode(self):
        node = super(DocumentDownloadableMediaMessageProtocolEntity, self).toProtocolTreeNode()
        mediaNode = node.getChild("media")

        mediaNode.setAttribute("title",  self.title)
        mediaNode.setAttribute("pages",     str(self.pages))

        return node

    def toProtobufMessage(self):
        document_message = DocumentMessage()
        document_message.url = self.url
        document_message.width = self.width
        document_message.height = self.height
        document_message.mime_type = self.mimeType
        document_message.file_sha256 = self.fileHash
        document_message.file_length = self.size
        document_message.caption = self.caption
        document_message.jpeg_thumbnail = self.preview
        document_message.media_key = self.mediaKey

        return image_message

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = DownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = DocumentDownloadableMediaMessageProtocolEntity
        mediaNode = node.getChild("media")
        entity.setDocumentProps(
            mediaNode.getAttributeValue("title"),
            mediaNode.getAttributeValue("pages"),
        )
        return entity
