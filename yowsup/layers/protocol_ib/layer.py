from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import *
import logging

logger = logging.getLogger(__name__)

class YowIbProtocolLayer(YowProtocolLayer):

    def __init__(self):
        handleMap = {
            "ib": (self.recvIb, self.sendIb),
            "iq": (None, self.sendIb)
        }
        super(YowIbProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Ib Layer"

    def sendIb(self, entity):
        if entity.__class__ == CleanIqProtocolEntity:
            self.toLower(entity.toProtocolTreeNode())

    def recvIb(self, node):
        if node.getChild("dirty"):
            self.toUpper(DirtyIbProtocolEntity.fromProtocolTreeNode(node))
        elif node.getChild("offline"):
            self.toUpper(OfflineIbProtocolEntity.fromProtocolTreeNode(node))
        elif node.getChild("account"):
            self.toUpper(AccountIbProtocolEntity.fromProtocolTreeNode(node))
        elif node.getChild("edge_routing"):
            logger.warning("ignoring edge_routing ib node for now")
        elif node.getChild("attestation"):
            logger.warning("ignoring attestation ib node for now")
        else:
            raise ValueError("Unkown ib node %s" % node)

