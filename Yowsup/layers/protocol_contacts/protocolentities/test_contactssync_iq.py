from .contactssync_iq import ContactsSyncIqProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.layers.protocol_iq.protocolentities.test_iq import IqProtocolEntityTest

class ContactsSyncIqProtocolEntityTest(IqProtocolEntityTest):
    def setUp(self):
        super(ContactsSyncIqProtocolEntityTest, self).setUp()
        self.ProtocolEntity = ContactsSyncIqProtocolEntity

        syncNodeAttrs = {
            "mode":     "full",
            "context":  "registration",
            "sid":      "SID",
            "index":    "0",
            "last":     "true"
        }
        numbers = ["123456", "654321"]

        users = [ProtocolTreeNode("user", {}, None, number) for number in numbers]
        syncNode = ProtocolTreeNode("sync", syncNodeAttrs, users, None)

        self.node.addChild(syncNode)