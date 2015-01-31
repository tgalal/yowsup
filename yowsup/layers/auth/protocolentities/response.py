from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class ResponseProtocolEntity(ProtocolEntity):
    schema = (__file__, "schemas/response.xsd")
    def __init__(self, data):
        super(ResponseProtocolEntity, self).__init__("response")
        self.xmlns = "urn:ietf:params:xml:ns:xmpp-sasl"
        self.data = data
    
    def toProtocolTreeNode(self):
        return self._createProtocolTreeNode(attributes={"xmlns": self.xmlns}, children = None, data = self.data)

    @staticmethod
    def fromProtocolTreeNode(node):
        return ResponseProtocolEntity(node.getData())