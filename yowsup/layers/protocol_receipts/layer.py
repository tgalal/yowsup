from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import *
class YowReceiptProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "receipt": (self.recvReceiptNode, self.sendReceiptEntity)
        }
        super(YowReceiptProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Receipt Layer"

    def sendReceiptEntity(self, entity):
        self.entityToLower(entity)

    def recvReceiptNode(self, node):
        self.toUpper(IncomingReceiptProtocolEntity.fromProtocolTreeNode(node))


