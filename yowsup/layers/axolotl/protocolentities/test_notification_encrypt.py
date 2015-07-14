from yowsup.layers.protocol_notifications.protocolentities.test_notification import NotificationProtocolEntityTest
from yowsup.layers.axolotl.protocolentities import EncryptNotification
from yowsup.structs import ProtocolTreeNode
class TestEncryptNotification(NotificationProtocolEntityTest):
    def setUp(self):
        super(TestEncryptNotification, self).setUp()
        self.ProtocolEntity = EncryptNotification
        self.node.addChild(ProtocolTreeNode("count", {"value": "9"}))