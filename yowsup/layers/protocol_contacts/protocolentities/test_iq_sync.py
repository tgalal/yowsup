from yowsup.layers.protocol_contacts.protocolentities.iq_sync import SyncIqProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest

class SyncIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(SyncIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = SyncIqProtocolEntity

        syncNodeAttrs = {
            "sid":      "SID",
            "index":    "0",
            "last":     "true"
        }
        syncNode = ProtocolTreeNode("sync", syncNodeAttrs)
        self.node.addChild(syncNode)