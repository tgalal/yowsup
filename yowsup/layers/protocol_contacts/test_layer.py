from yowsup.layers import YowProtocolLayerTest
from yowsup.layers.protocol_contacts import YowContactsIqProtocolLayer
from yowsup.layers.protocol_contacts.protocolentities.test_notification_contact_add import entity as addEntity
from yowsup.layers.protocol_contacts.protocolentities.test_notification_contact_update import entity as updateEntity
from yowsup.layers.protocol_contacts.protocolentities.test_notification_contact_remove import entity as removeEntity
from yowsup.layers.protocol_contacts.protocolentities.test_iq_sync_result import entity as syncResultEntity
from yowsup.layers.protocol_contacts.protocolentities.test_iq_sync_get import entity as syncGetEntity

class YowContactsIqProtocolLayerTest(YowProtocolLayerTest, YowContactsIqProtocolLayer):
    def setUp(self):
        YowContactsIqProtocolLayer.__init__(self)

    def test_sync(self):
        self.assertSent(syncGetEntity)

    def test_syncResult(self):
        self.assertReceived(syncResultEntity)

    def test_notificationAdd(self):
        self.assertReceived(addEntity)

    def test_notificationUpdate(self):
        self.assertReceived(updateEntity)

    def test_notificationRemove(self):
        self.assertReceived(removeEntity)
