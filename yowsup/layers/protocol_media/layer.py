from yowsup.layers import YowProtocolLayer
from .protocolentities import ImageDownloadableMediaMessageProtocolEntity
from .protocolentities import AudioDownloadableMediaMessageProtocolEntity
from .protocolentities import VideoDownloadableMediaMessageProtocolEntity
from .protocolentities import DocumentDownloadableMediaMessageProtocolEntity
from .protocolentities import StickerDownloadableMediaMessageProtocolEntity
from .protocolentities import LocationMediaMessageProtocolEntity
from .protocolentities import ContactMediaMessageProtocolEntity
from .protocolentities import ResultRequestUploadIqProtocolEntity
from .protocolentities import MediaMessageProtocolEntity
from .protocolentities import ExtendedTextMediaMessageProtocolEntity
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity, ErrorIqProtocolEntity
import logging

logger = logging.getLogger(__name__)


class YowMediaProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "message": (self.recvMessageStanza, self.sendMessageEntity),
            "iq": (self.recvIq, self.sendIq)
        }
        super(YowMediaProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Media Layer"

    def sendMessageEntity(self, entity):
        if entity.getType() == "media":
            self.entityToLower(entity)

    def recvMessageStanza(self, node):
        if node.getAttributeValue("type") == "media":
            mediaNode = node.getChild("proto")
            if mediaNode.getAttributeValue("mediatype") == "image":
                entity = ImageDownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
            elif mediaNode.getAttributeValue("mediatype") == "sticker":
                entity = StickerDownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
            elif mediaNode.getAttributeValue("mediatype") in ("audio", "ptt"):
                entity = AudioDownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
            elif mediaNode.getAttributeValue("mediatype") in ("video", "gif"):
                entity = VideoDownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
            elif mediaNode.getAttributeValue("mediatype") == "location":
                entity = LocationMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
            elif mediaNode.getAttributeValue("mediatype") == "contact":
                entity = ContactMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
            elif mediaNode.getAttributeValue("mediatype") == "document":
                entity = DocumentDownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
            elif mediaNode.getAttributeValue("mediatype") == "url":
                entity = ExtendedTextMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
            else:
                logger.warn("Unsupported mediatype: %s, will send receipts" % mediaNode.getAttributeValue("mediatype"))
                self.toLower(MediaMessageProtocolEntity.fromProtocolTreeNode(node).ack(True).toProtocolTreeNode())

    def sendIq(self, entity):
        """
        :type entity: IqProtocolEntity
        """
        if entity.getType() == IqProtocolEntity.TYPE_SET and entity.getXmlns() == "w:m":
            #media upload!
            self._sendIq(entity, self.onRequestUploadSuccess, self.onRequestUploadError)

    def recvIq(self, node):
        """
        :type node: ProtocolTreeNode
        """

    def onRequestUploadSuccess(self, resultNode, requestUploadEntity):
        self.toUpper(ResultRequestUploadIqProtocolEntity.fromProtocolTreeNode(resultNode))

    def onRequestUploadError(self, errorNode, requestUploadEntity):
        self.toUpper(ErrorIqProtocolEntity.fromProtocolTreeNode(errorNode))
