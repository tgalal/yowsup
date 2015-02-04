from yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest
from yowsup.layers.axolotl.protocolentities import SetKeysIqProtocolEntity
from yowsup.structs import ProtocolTreeNode
class SetKeysIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(SetKeysIqProtocolEntityTest, self).setUp()
        # self.ProtocolEntity = SetKeysIqProtocolEntity
        #
        # regNode = ProtocolTreeNode("registration", data = "abcd")
        # idNode = ProtocolTreeNode("identity", data = "efgh")
        # typeNode = ProtocolTreeNode("type", data = "ijkl")
        # listNode = ProtocolTreeNode("list")
        # for i in range(0, 2):
        #     keyNode = ProtocolTreeNode("key", children=[
        #         ProtocolTreeNode("id", data = "id_%s" % i),
        #         ProtocolTreeNode("value", data = "val_%s" % i)
        #     ])
        #     listNode.addChild(keyNode)
        #
        # self.node.addChildren([regNode, idNode, typeNode, listNode])
