from yowsup.structs import ProtocolEntity, ProtocolTreeNode
class FailureProtocolEntity(ProtocolEntity):

    def __init__(self, reason):
        super(FailureProtocolEntity, self).__init__("failure")
        self.reason = reason

    def __str__(self):
        out  = "Failure:\n"
        out += "Reason: %s\n" % self.reason
        return out

    def getReason(self):
        return self.reason

    def toProtocolTreeNode(self):
        reasonNode = ProtocolTreeNode(self.reason, {})
        return self._createProtocolTreeNode({}, children = [reasonNode])

    @staticmethod
    def fromProtocolTreeNode(node):
        return FailureProtocolEntity( node.getAllChildren()[0].tag )