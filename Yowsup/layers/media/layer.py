from Yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import ImageDownloadableMediaMessageProtocolEntity
class YowMediaProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "message": self.handleMessageStanza
        }
        super(YowMediaProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Messages Layer"

    def send(self, data):
        self.toLower(data)

    ###recieved node handlers handlers
    def handleMessageStanza(self, node):
        if node.getAttributeValue("type") == "media":
            mediaNode = node.getChild("media")
            if mediaNode.getAttributeValue("type") == "image":
                entity = ImageDownloadableMediaMessageProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)
