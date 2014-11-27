from yowsup.layers.auth.protocolentities.success import SuccessProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest

class SuccessProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = SuccessProtocolEntity
        attribs = {
            "status": "active",
            "kind": "free",
            "creation": "1234",
            "expiration": "1446578937",
            "props": "2",
            "t": "1415470561"
        }
        self.node = ProtocolTreeNode("success", attribs, None, "dummydata")