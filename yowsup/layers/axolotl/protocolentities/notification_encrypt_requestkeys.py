from yowsup.common import YowConstants
from yowsup.layers.protocol_notifications.protocolentities import NotificationProtocolEntity
from yowsup.structs import ProtocolTreeNode


class RequestKeysEncryptNotification(NotificationProtocolEntity):
    """
    <notification t="1419824928" id="2451228097" from="s.whatsapp.net" type="encrypt">
        <count value="9">
        </count>
    </notification>
    """
    def __init__(self, count, timestamp, _id = None, notify = None, offline = None):
        super(RequestKeysEncryptNotification, self).__init__(
            "encrypt", _id, YowConstants.WHATSAPP_SERVER, timestamp, notify, offline
        )
        self._count = count

    @property
    def count(self):
        return self._count

    @count.setter
    def count(self, value):
        self._count = value

    def toProtocolTreeNode(self):
        node = super(RequestKeysEncryptNotification, self).toProtocolTreeNode()
        count_node = ProtocolTreeNode("count", {"value": str(self.count)})
        node.addChild(count_node)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = NotificationProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = RequestKeysEncryptNotification
        entity.count = node.getChild("count")["value"]
        return entity
