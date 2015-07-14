from yowsup.layers.protocol_notifications.protocolentities.notification_picture_delete import DeletePictureNotificationProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_notifications.protocolentities.test_notification_picture import PictureNotificationProtocolEntityTest

class DeletePictureNotificationProtocolEntityTest(PictureNotificationProtocolEntityTest):
    def setUp(self):
        super(DeletePictureNotificationProtocolEntityTest, self).setUp()
        self.ProtocolEntity = DeletePictureNotificationProtocolEntity
        deleteNode = ProtocolTreeNode("delete", {"jid": "DELETE_JID"}, None, None)
        self.node.addChild(deleteNode)
