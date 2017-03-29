from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import TextMessageProtocolEntity


class YowMessagesProtocolLayer(YowProtocolLayer):

    EVENT_MESSAGE_RECEIVED = \
    "org.openwhatsapp.yowsup.event.protocol_messages.received"

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
        self.getStack().broadcastEvent(
            YowLayerEvent(
                YowMessagesProtocolLayer.EVENT_MESSAGE_RECEIVED,
                reason="Message received"))
        if node.getAttributeValue("type") == "text":
            entity = TextMessageProtocolEntity.fromProtocolTreeNode(node)
            self.toUpper(entity)
