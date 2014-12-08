from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import ImageDownloadableMediaMessageProtocolEntity
from .protocolentities import LocationMediaMessageProtocolEntity

class YowMediaProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "message": (self.recvMessageStanza, self.sendMessageEntity)
        }
        super(YowMediaProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Media Layer"

    def sendMessageEntity(self, entity):
        if entity.getType() == "media":
            self.entityToLower(entity)

    ###recieved node handlers handlers
    def recvMessageStanza(self, node):
        if node.getAttributeValue("type") == "media":
            mediaNode = node.getChild("media")
            if mediaNode.getAttributeValue("type") == "image":
                entity = ImageDownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)    
            if mediaNode.getAttributeValue("type") == "location":
                entity = LocationMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
