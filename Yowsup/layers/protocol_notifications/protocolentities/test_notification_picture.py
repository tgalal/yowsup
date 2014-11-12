from .notification_picture import PictureNotificationProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from .test_notification import NotificationProtocolEntityTest

class PictureNotificationProtocolEntityTest(NotificationProtocolEntityTest):
    def setUp(self):
        super(PictureNotificationProtocolEntityTest, self).setUp()
        self.ProtocolEntity = PictureNotificationProtocolEntity
