from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from .protocolentities import *
from yowsup.layers.protocol_acks.protocolentities import OutgoingAckProtocolEntity
import logging


logger = logging.getLogger(__name__)


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
                self.toUpper(SetPictureNotificationProtocolEntity.fromProtocolTreeNode(node))
            elif node.getChild("delete"):
                self.toUpper(DeletePictureNotificationProtocolEntity.fromProtocolTreeNode(node))
            else:
                self.raiseErrorForNode(node)
        elif node["type"] == "status":
            self.toUpper(StatusNotificationProtocolEntity.fromProtocolTreeNode(node))
        elif node["type"] in ["contacts", "subject", "w:gp2"]:
            # Implemented in respectively the protocol_contacts and protocol_groups layer
            pass
        else:
            logger.warning("Unsupported notification type: %s " % node["type"])
            logger.debug("Unsupported notification node: %s" % node)

        ack = OutgoingAckProtocolEntity(node["id"], "notification", node["type"], node["from"], participant=node["participant"])
        self.toLower(ack.toProtocolTreeNode())






