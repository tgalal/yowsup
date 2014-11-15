from Yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import CreateGroupsIqProtocolEntity
class YowGroupsProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "iq": (self.recvIq, self.sendIq)
        }
        super(YowGroupsProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Groups Iq Layer"

    def sendIq(self, entity):
        if entity.__class__ == CreateGroupsIqProtocolEntity:
            self.entityToLower(entity)

    def recvIq(self, node):
        return

