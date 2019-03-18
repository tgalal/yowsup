from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class SuccessProtocolEntity(ProtocolEntity):
    def __init__(self, creation, props, t, location):
        super(SuccessProtocolEntity, self).__init__("success")
        self.location = location
        self.creation = int(creation)
        self.props = props
        self.t = int(t) ##whatever that is !

    def __str__(self):
        out  = "Account:\n"
        out += "Location: %s\n" % self.location
        out += "Creation: %s\n" % self.creation
        out += "Props: %s\n" % self.props
        out += "t: %s\n" % self.t
        return out

    def toProtocolTreeNode(self):
        attributes = {
            "location"      :  self.location,
            "creation"    :    str(self.creation),
            "props"       :    self.props,
            "t"           :    str(self.t)
        }
        return self._createProtocolTreeNode(attributes)

    @staticmethod
    def fromProtocolTreeNode(node):
        return SuccessProtocolEntity(
            node.getAttributeValue("creation"),
            node.getAttributeValue("props"),
            node.getAttributeValue("t"),
            node.getAttributeValue("location")
            )