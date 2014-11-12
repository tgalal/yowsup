from .notification_picture_set import SetPictureNotificationProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from .test_notification_picture import PictureNotificationProtocolEntityTest

class SetPictureNotificationProtocolEntityTest(PictureNotificationProtocolEntityTest):
    def setUp(self):
        super(SetPictureNotificationProtocolEntityTest, self).setUp()
        self.ProtocolEntity = SetPictureNotificationProtocolEntity
        setNode = ProtocolTreeNode("set", {"id": "SET_JID", "jid": "123"}, None, None)
        self.node.addChild(setNode)
