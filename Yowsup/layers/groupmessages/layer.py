from Yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from Yowsup.layers.messages import YowMessagesProtocolLayer
from .protocolentities import TextGroupMessageProtocolEntity
class YowGroupMessagesProtocolLayer(YowMessagesProtocolLayer):
    def __str__(self):
        return "Group Messages Protocol Layer"

    def send(self, data):
        self.toLower(data)

    ###recieved node handlers handlers
    def handleMessageStanza(self, node):
        if self.isGroupJid(node.getAttributeValue("from")):
            if node.getAttributeValue("type") == "text":
                entity = TextGroupMessageProtocolEntity.fromProtocolTreeNode(node)
                print(entity)
