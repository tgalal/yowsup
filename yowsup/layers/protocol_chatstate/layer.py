from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import * 
class YowChatstateProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "chatstate": (self.recvChatstateNode, self.sendChatstateEntity)
        }
        super(YowChatstateProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Chatstate Layer"

    def sendChatstateEntity(self, entity):
        self.entityToLower(entity)

    def recvChatstateNode(self, node):
        self.toUpper(IncomingChatstateProtocolEntity.fromProtocolTreeNode(node))
