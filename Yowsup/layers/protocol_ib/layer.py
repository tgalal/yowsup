from Yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import *
class YowIbProtocolLayer(YowProtocolLayer):

    def __init__(self):
        handleMap = {
            "ib": (self.recvIb, self.sendIb)
        }
        super(YowGroupsProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Groups Ib Layer"

    def sendIb(self, entity):
        return

    def recvIb(self, node):
        if node.getChild("dirty"):
            self.toUpper(DirtyIbProtocolEntity.fromProtocolTreeNode(node))
        else:
            raise ValueError("Unkown ib node %s" % node)

