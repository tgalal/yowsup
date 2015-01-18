from yowsup.layers.protocol_groups.protocolentities.iq_result_groups_list import ListGroupsResultIqProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
from yowsup.layers.protocol_groups.structs import Group
import unittest
import time

entity = ListGroupsResultIqProtocolEntity(
    [
        Group("1234-456", "owner@s.whatsapp.net", "subject", "sOwnerJid@s.whatsapp.net", int(time.time()), int(time.time())),
        Group("4321-456", "owner@s.whatsapp.net", "subject", "sOwnerJid@s.whatsapp.net", int(time.time()), int(time.time()))
    ]
)

class ListGroupsResultIqProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = ListGroupsResultIqProtocolEntity
        self.node = entity.toProtocolTreeNode()
