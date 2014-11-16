from Yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import *
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
            self.toUpper(PictureNotificationProtocolEntity.fromProtocolTreeNode(node))
        elif node["type"] == "status":
            self.toUpper(StatusNotificationProtocolEntity.fromProtocolTreeNode(node))
        else:
            raise ValueError("Unimplemented notification type %s " % node)

