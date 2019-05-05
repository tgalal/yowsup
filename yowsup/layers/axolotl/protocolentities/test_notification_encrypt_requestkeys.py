from yowsup.layers.protocol_notifications.protocolentities.test_notification import NotificationProtocolEntityTest
from yowsup.layers.axolotl.protocolentities import RequestKeysEncryptNotification
from yowsup.structs import ProtocolTreeNode


class TestRequestKeysEncryptNotification(NotificationProtocolEntityTest):
    def setUp(self):
        super(TestRequestKeysEncryptNotification, self).setUp()
        self.ProtocolEntity = RequestKeysEncryptNotification
        self.node.addChild(ProtocolTreeNode("count", {"value": "9"}))