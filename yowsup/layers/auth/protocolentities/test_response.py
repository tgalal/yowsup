from yowsup.layers.auth.protocolentities.response import ResponseProtocolEntity
from yowsup.structs import ProtocolTreeNode
from yowsup.structs.protocolentity import ProtocolEntityTest

class ResponseProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = ResponseProtocolEntity
        attribs = {
            "xmlns": "urn:ietf:params:xml:ns:xmpp-sasl"
        }
        self.node = ProtocolTreeNode("response", attribs, None, "dummydata")