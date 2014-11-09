from Yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import TextMessageProtocolEntity
class YowMessagesProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "message": self.handleMessageStanza
        }
        super(YowMessagesProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Messages Layer"

    def send(self, data):
        self.toLower(data)

    ###recieved node handlers handlers
    def handleMessageStanza(self, node):
        if not self.isGroupJid(node.getAttributeValue("from")):
            if node.getAttributeValue("type") == "text":
                entity = TextMessageProtocolEntity.fromProtocolTreeNode(node)
                print(entity)

