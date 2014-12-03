from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import *
class YowPresenceProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "presence": (self.recvPresence, self.sendPresence)
        }
        super(YowPresenceProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Presence Layer"

    def sendPresence(self, entity):
        self.entityToLower(entity)

    def recvPresence(self, node):
        pass
        #self.toUpper(IncomingAckProtocolEntity.fromProtocolTreeNode(node))
