from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
class SuccessProtocolEntity(ProtocolEntity):
    def __init__(self, status, kind, creation, expiration, props, t, nonce = None):
        super(SuccessProtocolEntity, self).__init__("success")
        self.status = status
        self.kind = kind
        self.creation = long(creation)
        self.expiration = long(expiration)
        self.props = props
        self.nonce = nonce
        self.t = long(t) ##whatever that is !

    def toProtocolTreeNode(self):
        attributes = {
            "status"      :    self.status,
            "kind"        :    self.kind,
            "creation"    :    str(self.creation),
            "expiration"  :    str(self.expiration),
            "props"       :    self.props,
            "t"           :    self.t
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