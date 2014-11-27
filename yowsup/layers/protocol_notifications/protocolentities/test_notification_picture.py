from yowsup.layers.protocol_notifications.protocolentities.notification_picture import PictureNotificationProtocolEntity
from yowsup.layers.protocol_notifications.protocolentities.test_notification import NotificationProtocolEntityTest

class PictureNotificationProtocolEntityTest(NotificationProtocolEntityTest):
    def setUp(self):
        super(PictureNotificationProtocolEntityTest, self).setUp()
        self.ProtocolEntity = PictureNotificationProtocolEntity
