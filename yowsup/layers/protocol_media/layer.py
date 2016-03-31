from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import DocumentDownloadableMediaMessageProtocolEntity
from .protocolentities import ImageDownloadableMediaMessageProtocolEntity
from .protocolentities import AudioDownloadableMediaMessageProtocolEntity
from .protocolentities import VideoDownloadableMediaMessageProtocolEntity
from .protocolentities import UrlMediaMessageProtocolEntity
from .protocolentities import LocationMediaMessageProtocolEntity
from .protocolentities import VCardMediaMessageProtocolEntity
from .protocolentities import RequestUploadIqProtocolEntity, ResultRequestUploadIqProtocolEntity
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity, ErrorIqProtocolEntity

class YowMediaProtocolLayer(YowProtocolLayer):

    # EVENT_REQUEST_UPLOAD = "org.openwhatsapp.org.yowsup.event.protocol_media.request_upload"

    def __init__(self):
        handleMap = {
            "message": (self.recvMessageStanza, self.sendMessageEntity),
            "iq": (self.recvIq, self.sendIq)
        }
        super(YowMediaProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Media Layer"

    # def onEvent(self, yowLayerEvent):
    #     if yowLayerEvent.getArg(self.__class__.EVENT_REQUEST_UPLOAD):
    #         fpath = yowLayerEvent.getArg("file")
    #         _type = yowLayerEvent.getArg("type")
    #         assert fpath and _type, "Must specify 'file' and 'type' in EVENT_REQUEST_UPLOAD args"
    #         entity = RequestUploadIqProtocolEntity(_type, filePath=fpath)
    #         self._sendIq(entity, self.onRequestUploadSuccess, self.onRequestUploadError)


    def sendMessageEntity(self, entity):
        if entity.getType() == "media":
            self.entityToLower(entity)

    def recvMessageStanza(self, node):
        if node.getAttributeValue("type") == "media":
            mediaNode = node.getChild("media")
            if mediaNode.getAttributeValue("type") == "image":
                entity = ImageDownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
            elif mediaNode.getAttributeValue("type") == "audio":
                entity = AudioDownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
            elif mediaNode.getAttributeValue("type") == "video":
                entity = VideoDownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
            elif mediaNode.getAttributeValue("type") == "location":
                entity = LocationMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
            elif mediaNode.getAttributeValue("type") == "vcard":
                entity = VCardMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
            elif mediaNode.getAttributeValue("type") == "url":
                entity = UrlMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
            elif mediaNode.getAttributeValue("type") == "document":
                entity = DocumentDownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)

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
