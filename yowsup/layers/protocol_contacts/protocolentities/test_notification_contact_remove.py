from yowsup.layers.protocol_contacts.protocolentities import RemoveContactNotificationProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import time
import unittest

entity = RemoveContactNotificationProtocolEntity("1234", "jid@s.whatsapp.net",
                                                 int(time.time()), "notify", False, "contactjid@s.whatsapp.net")

class RemoveContactNotificationProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = RemoveContactNotificationProtocolEntity
        self.node = entity.toProtocolTreeNode()
