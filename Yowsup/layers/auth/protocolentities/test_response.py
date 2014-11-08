from .response import ResponseProtocolEntity
from Yowsup.structs import ProtocolTreeNode
from Yowsup.structs.protocolentity import ProtocolEntityTest

class ResponseProtocolEntityTest(ProtocolEntityTest):
    def setUp(self):
        self.ProtocolEntity = ResponseProtocolEntity
        attribs = {
            "xmlns": "urn:ietf:params:xml:ns:xmpp-sasl"
        }
        self.node = ProtocolTreeNode("response", attribs, None, "dummydata")