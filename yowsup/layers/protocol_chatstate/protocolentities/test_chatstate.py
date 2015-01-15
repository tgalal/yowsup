from yowsup.layers.protocol_chatstate.protocolentities.chatstate import ChatstateProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest
import unittest

class ChatstateProtocolEntityTest(ProtocolEntityTest, unittest.TestCase):
    def setUp(self):
        self.ProtocolEntity = ChatstateProtocolEntity
        self.node = ProtocolTreeNode("chatstate")
        self.node.addChild(ProtocolTreeNode('composing'))
