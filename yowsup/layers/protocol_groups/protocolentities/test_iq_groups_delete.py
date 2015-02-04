from yowsup.structs.protocolentity import ProtocolEntityTest
from yowsup.layers.protocol_groups.protocolentities import DeleteGroupsIqProtocolEntity
import unittest

entity = DeleteGroupsIqProtocolEntity("123-456@g.us")

class DeleteGroupsIqProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = DeleteGroupsIqProtocolEntity
        self.node = entity.toProtocolTreeNode()