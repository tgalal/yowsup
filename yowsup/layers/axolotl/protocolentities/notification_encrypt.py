from yowsup.common import YowConstants
from yowsup.layers.protocol_notifications.protocolentities import NotificationProtocolEntity
from yowsup.structs import ProtocolTreeNode
class EncryptNotification(NotificationProtocolEntity):
    """
    <notification t="1419824928" id="2451228097" from="s.whatsapp.net" type="encrypt">
        <count value="9">
        </count>
    </notification>
    """
    def __init__(self, count, timestamp, _id = None, notify = None, offline = None):
        super(EncryptNotification, self).__init__("encrypt", _id, YowConstants.WHATSAPP_SERVER, timestamp, notify, offline)
        self.setProps(count)

    def setProps(self, count):
        self.count = int(count)

    def getCount(self):
        return self.count

    def toProtocolTreeNode(self):
        node = super(EncryptNotification, self).toProtocolTreeNode()
        countNode = ProtocolTreeNode("count", {"value": str(self.count)})
        node.addChild(countNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = NotificationProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = EncryptNotification
        entity.setProps(node.getChild("count")["value"])
        return entity