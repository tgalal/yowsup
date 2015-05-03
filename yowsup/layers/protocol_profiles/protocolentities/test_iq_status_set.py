from yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest
from yowsup.layers.protocol_profiles.protocolentities import SetStatusIqProtocolEntity
from yowsup.structs import ProtocolTreeNode
import unittest
from yowsup.structs.protocolentity import ProtocolEntityTest
# class SetStatusIqProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
#     def setUp(self):
#         #super(SetStatusIqProtocolEntityTest, self).setUp()
#         self.ProtocolEntity = SetStatusIqProtocolEntity
#         #statusNode = ProtocolTreeNode("status", {}, [], "Hey there, I'm using WhatsApp")
#         self.node = SetStatusIqProtocolEntity("HELLO", "123").toProtocolTreeNode()
#         # self.xml = SetStatusIqProtocolEntity("HELLO", "123").toProtocolTreeNode().__str__()
