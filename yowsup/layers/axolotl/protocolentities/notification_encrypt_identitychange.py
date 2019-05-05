from yowsup.common import YowConstants
from yowsup.layers.protocol_notifications.protocolentities import NotificationProtocolEntity
from yowsup.structs import ProtocolTreeNode


class IdentityChangeEncryptNotification(NotificationProtocolEntity):
    """
    <notification t="1419824928" id="2451228097" from="s.whatsapp.net" type="encrypt">
        <identity />
    </notification>
    """
    def __init__(self, timestamp, _id = None, notify = None, offline = None):
        super(IdentityChangeEncryptNotification, self).__init__(
            "encrypt", _id, YowConstants.WHATSAPP_SERVER, timestamp, notify, offline
        )

    def toProtocolTreeNode(self):
        node = super(IdentityChangeEncryptNotification, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("identity"))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = NotificationProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = IdentityChangeEncryptNotification
        return entity
