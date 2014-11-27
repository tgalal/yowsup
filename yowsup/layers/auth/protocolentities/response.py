from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class ResponseProtocolEntity(ProtocolEntity):
    def __init__(self, data, xmlns = "urn:ietf:params:xml:ns:xmpp-sasl"):
        super(ResponseProtocolEntity, self).__init__("response")
        self.xmlns = xmlns
        self.data = data
    
    def toProtocolTreeNode(self):
        return self._createProtocolTreeNode({"xmlns": self.xmlns}, children = None, data = self.data)

    @staticmethod
    def fromProtocolTreeNode(node):
        return ResponseProtocolEntity(node.getData(), node.getAttributeValue("xmlns"))