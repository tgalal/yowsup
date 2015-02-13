from yowsup.structs import ProtocolEntity
class AuthProtocolEntity(ProtocolEntity):
    schema = (__file__, "schemas/auth.xsd")
    def __init__(self, user, mechanism = "WAUTH-2", passive = False, nonce = None):
        super(AuthProtocolEntity, self).__init__("auth")
        self.user = user
        self.mechanism = mechanism
        self.passive = passive
        self.nonce = nonce
    
    def toProtocolTreeNode(self):
        attributes = {
            "user"      :    self.user,
            "mechanism" :    self.mechanism,
            "passive"   :    "true" if self.passive else "false"
        }
        return self._createProtocolTreeNode(attributes, children = None, data = self.nonce)

    @staticmethod
    def fromProtocolTreeNode(node):
        return AuthProtocolEntity(
            node.getAttributeValue("user"),
            node.getAttributeValue("mechanism"),
            node.getAttributeValue("passive") != "false",
            node.getData()
            )