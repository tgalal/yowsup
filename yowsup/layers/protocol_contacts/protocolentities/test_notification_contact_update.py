from yowsup.layers.protocol_contacts.protocolentities import UpdateContactNotificationProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import time
import unittest

entity = UpdateContactNotificationProtocolEntity("1234", "jid@s.whatsapp.net",
                                                 int(time.time()), "notify", False,"contactjid@s.whatsapp.net")

class UpdateContactNotificationProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = UpdateContactNotificationProtocolEntity
        self.node = entity.toProtocolTreeNode()
