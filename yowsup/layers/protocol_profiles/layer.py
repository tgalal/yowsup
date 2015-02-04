from yowsup.layers import  YowProtocolLayer
from .protocolentities import *
class YowProfilesProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "iq": (self.recvIq, self.sendIq)
        }
        super(YowProfilesProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Profiles Layer"

    def sendIq(self, entity):
        if entity.getXmlns() == "w:profile:picture":
            self.toLower(entity.toProtocolTreeNode())

    def recvIq(self, node):
        if node["type"] == "result":
            pictureNode = node.getChild("picture")
            if pictureNode is not None:
                entity = PictureIqProtocolEntity.fromProtocolTreeNode(node)
                self.toUpper(entity)

