from yowsup.layers.protocol_contacts.protocolentities.iq_sync_get import GetSyncIqProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_contacts.protocolentities.test_iq_sync import SyncIqProtocolEntityTest

class GetSyncIqProtocolEntityTest(SyncIqProtocolEntityTest):
    def setUp(self):
        super(GetSyncIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = GetSyncIqProtocolEntity

        users = [
            ProtocolTreeNode("user", data = "abc"),
            ProtocolTreeNode("user", data =  "xyz")
        ]

        syncNode = self.node.getChild("sync")
        syncNode.setAttribute("mode", GetSyncIqProtocolEntity.MODE_DELTA)
        syncNode.setAttribute("context", GetSyncIqProtocolEntity.CONTEXT_INTERACTIVE)
        syncNode.addChildren(users)
