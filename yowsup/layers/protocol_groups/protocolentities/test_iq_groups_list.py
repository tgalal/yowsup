from yowsup.layers.protocol_groups.protocolentities.iq_groups_list import ListGroupsIqProtocolEntity
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

entity = ListGroupsIqProtocolEntity()

class ListGroupsIqProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = ListGroupsIqProtocolEntity
        self.node = entity.toProtocolTreeNode()
