from yowsup.layers.protocol_contacts.protocolentities.iq_sync_result import ResultSyncIqProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_contacts.protocolentities.test_iq_sync import SyncIqProtocolEntityTest

class ResultSyncIqProtocolEntityTest(SyncIqProtocolEntityTest):
    def setUp(self):
        super(ResultSyncIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = ResultSyncIqProtocolEntity

        users = [
            ProtocolTreeNode("user", {"jid": "abc"}, data = "abc"),
            ProtocolTreeNode("user", {"jid": "xyz"}, data =  "xyz")
        ]
        invalids = ["aaaaa", "bbbbb"]

        syncNode = self.node.getChild("sync")
        syncNode.setAttribute("wait", "123456")
        syncNode.setAttribute("version", "654321")
        syncNode.addChild(ProtocolTreeNode("out", children = users))
        syncNode.addChild(ProtocolTreeNode("in", children = users))
        syncNode.addChild(ProtocolTreeNode("invalid", children = [ProtocolTreeNode("user", data = inv) for inv in invalids]))
