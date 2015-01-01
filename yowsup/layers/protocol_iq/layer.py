from yowsup.layers import  YowProtocolLayer
from yowsup.common import YowConstants
from .protocolentities import *
class YowIqProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "iq": (self.recvIq, self.sendIq)
        }
        super(YowIqProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Iq Layer"

    def onPong(self, protocolTreeNode, pingEntity):
        self.toUpper(ResultIqProtocolEntity.fromProtocolTreeNode(protocolTreeNode))

    def sendIq(self, entity):
        if entity.getXmlns() == "w:p":
            self._sendIq(entity, self.onPong)
        elif entity.getXmlns() in ("urn:xmpp:whatsapp:push", "w", "urn:xmpp:whatsapp:account", "encrypt"):
            self.toLower(entity.toProtocolTreeNode())

    def recvIq(self, node):
        if node["xmlns"] == "urn:xmpp:ping":
            entity = PongResultIqProtocolEntity(YowConstants.DOMAIN, node["id"])
            self.toLower(entity.toProtocolTreeNode())
