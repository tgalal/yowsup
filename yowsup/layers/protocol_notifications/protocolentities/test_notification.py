from yowsup.layers.protocol_notifications.protocolentities.notification import NotificationProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest

class NotificationProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = NotificationProtocolEntity
        attribs = {
            "t": "12345",
            "from": "from_jid",
            "offline": "0",
            "type": "notif_type",
            "id": "message-id",
            "notify": "notify_name"
        }
        self.node = ProtocolTreeNode("notification", attribs)