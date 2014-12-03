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

    def sendIq(self, entity):
        if entity.getXmlns() == "w:p":
            self.toLower(entity.toProtocolTreeNode())

    def recvIq(self, node):
        if node["xmlns"] == "urn:xmpp:ping":
            entity = PongResultIqProtocolEntity(YowConstants.DOMAIN, node["id"])
            self.toLower(entity.toProtocolTreeNode())
        elif node["type"] == "error":
            self.toUpper(ErrorIqProtocolEntity.fromProtocolTreeNode(node))
        elif node["type"] == "result" and not len(node.getAllChildren()):
            #allowing only unidentifiable result (has no children) iq through this layer. (ex: ping result)
            self.toUpper(ResultIqProtocolEntity.fromProtocolTreeNode(node))
