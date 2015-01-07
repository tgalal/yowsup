from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import *
class YowPrivacyProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "iq": (self.recvIq, self.sendIq)
        }
        super(YowPrivacyProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Privacy Layer"

    def sendIq(self, entity):
        if entity.getXmlns() == "jabber:iq:privacy":
            self.entityToLower(entity)

    def recvIq(self, node):
        pass
