from yowsup.layers import YowLayer, YowLayerEvent, YowProtocolLayer
from yowsup.common import YowConstants
from .protocolentities import *
class YowContactsIqProtocolLayer(YowProtocolLayer):
    def __init__(self):
        handleMap = {
            "iq": (self.recvIq, self.sendIq),
            "notification": (self.recvNotification, None)
        }
        super(YowContactsIqProtocolLayer, self).__init__(handleMap)

    def __str__(self):
        return "Iq Layer"

    def recvNotification(self, node):
        if node["type"] == "contacts":
            if node.getChild("remove"):
                self.toUpper(RemoveContactNotificationProtocolEntity.fromProtocolTreeNode(node))
            elif node.getChild("add"):
                self.toUpper(AddContactNotificationProtocolEntity.fromProtocolTreeNode(node))
            else:
                self.raiseErrorForNode(node)

    def recvIq(self, node):
        if node["type"] == "result" and node.getChild("sync"):
            self.toUpper(ResultSyncIqProtocolEntity.fromProtocolTreeNode(node))

    def sendIq(self, entity):
        if entity.getXmlns() == "urn:xmpp:whatsapp:sync":
            self.toLower(entity.toProtocolTreeNode())
