from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import *
from yowsup.layers.protocol_iq.protocolentities import ErrorIqProtocolEntity
class YowPresenceProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "presence": (self.recvPresence, self.sendPresence),
            "iq":       (None, self.sendIq)
        }
        super(YowPresenceProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Presence Layer"

    def sendPresence(self, entity):
        self.entityToLower(entity)

    def recvPresence(self, node):
        self.toUpper(PresenceProtocolEntity.fromProtocolTreeNode(node))

    def sendIq(self, entity):
        if entity.getXmlns() == LastseenIqProtocolEntity.XMLNS:
            self._sendIq(entity, self.onLastSeenSuccess, self.onLastSeenError)

    def onLastSeenSuccess(self, protocolTreeNode, lastSeenEntity):
        self.toUpper(ResultLastseenIqProtocolEntity.fromProtocolTreeNode(protocolTreeNode))

    def onLastSeenError(self, protocolTreeNode, lastSeenEntity):
        self.toUpper(ErrorIqProtocolEntity.fromProtocolTreeNode(protocolTreeNode))
