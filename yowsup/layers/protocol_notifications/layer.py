from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import *
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
class YowNotificationsProtocolLayer(YowProtocolLayer):

    def __init__(self):
        handleMap = {
            "notification": (self.recvNotification, self.sendNotification)
        }
        super(YowNotificationsProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "notification Ib Layer"

    def sendNotification(self, entity):
        if entity.getTag() == "notification":
            self.toLower(entity.toProtocolTreeNode())

    def recvNotification(self, node):
        if node["type"] == "picture":
            if node.getChild("set"):
                self.toUpper(PictureNotificationProtocolEntity.fromProtocolTreeNode(node))
            else:
                self.raiseErrorForNode(node)
        elif node["type"] == "status":
            self.toUpper(StatusNotificationProtocolEntity.fromProtocolTreeNode(node))
        elif node["type"] == "features":
            pass
        else:
            self.raiseErrorForNode(node)

        ack = OutgoingAckProtocolEntity(node["id"], "notification", node["type"])
        self.toLower(ack.toProtocolTreeNode())






