from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class AuthProtocolEntity(ProtocolEntity):
    def __init__(self, user, mechanism = "WAUTH-2", passive = False):
        super(AuthProtocolEntity, self).__init__("auth")
        self.user = user
        self.mechanism = mechanism
        self.passive = passive
    
    def toProtocolTreeNode(self):
        attributes = {
            "user"      :    self.user,
            "mechanism" :    self.mechanism,
            "passive"   :    "true" if self.passive else "false"
        }
        return self._createProtocolTreeNode(attributes, children = None, data = None)

    @staticmethod
    def fromProtocolTreeNode(node):
        return AuthProtocolEntity(
            node.getAttributeValue("user"),
            node.getAttributeValue("mechanism"),
            node.getAttributeValue("passive") != "false"
            )