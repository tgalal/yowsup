from .notification_status import StatusNotificationProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest
from .test_notification import NotificationProtocolEntityTest

class StatusNotificationProtocolEntityTest(NotificationProtocolEntityTest):
    def setUp(self):
        super(StatusNotificationProtocolEntityTest, self).setUp()
        self.ProtocolEntity = StatusNotificationProtocolEntity
        setNode = ProtocolTreeNode("set", {}, None, "status_data")
        self.node.addChild(setNode)
