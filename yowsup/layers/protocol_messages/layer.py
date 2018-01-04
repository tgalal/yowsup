from yowsup.layers import YowProtocolLayer
from .protocolentities import TextMessageProtocolEntity
class YowMessagesProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "message": (self.recvMessageStanza, self.sendMessageEntity)
        }
        super(YowMessagesProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Messages Layer"

    def sendMessageEntity(self, entity):
        if entity.getType() == "text":
            self.entityToLower(entity)

    ###recieved node handlers handlers
    def recvMessageStanza(self, node):
        decNode = node.getChild("dec")

        if decNode:
           if decNode and decNode["mediatype"] is None:
               self.toUpper(TextMessageProtocolEntity.fromDecryptedMessageProtocolTreeNode(node))

        elif node.getAttributeValue("type") == "text" and node.getChild("body"):
            entity = TextMessageProtocolEntity.fromProtocolTreeNode(node)
            self.toUpper(entity) 

