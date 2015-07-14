from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class SuccessProtocolEntity(ProtocolEntity):
    def __init__(self, status, kind, creation, expiration, props, t, nonce = None):
        super(SuccessProtocolEntity, self).__init__("success")
        self.status = status
        self.kind = kind
        self.creation = int(creation)
        self.expiration = int(expiration)
        self.props = props
        self.nonce = nonce
        self.t = int(t) ##whatever that is !

    def __str__(self):
        out  = "Account:\n"
        out += "Status: %s\n" % self.status
        out += "Kind: %s\n" % self.kind
        out += "Creation: %s\n" % self.creation
        out += "Expiration: %s\n" % self.expiration
        out += "Props: %s\n" % self.props
        out += "t: %s\n" % self.t
        return out

    def toProtocolTreeNode(self):
        attributes = {
            "status"      :    self.status,
            "kind"        :    self.kind,
            "creation"    :    str(self.creation),
            "expiration"  :    str(self.expiration),
            "props"       :    self.props,
            "t"           :    str(self.t)
        }
        return self._createProtocolTreeNode(attributes, children = None, data = self.nonce)

    @staticmethod
    def fromProtocolTreeNode(node):
        return SuccessProtocolEntity(
            node.getAttributeValue("status"),
            node.getAttributeValue("kind"),
            node.getAttributeValue("creation"),
            node.getAttributeValue("expiration"),
            node.getAttributeValue("props"),
            node.getAttributeValue("t"),
            node.getData()
            )