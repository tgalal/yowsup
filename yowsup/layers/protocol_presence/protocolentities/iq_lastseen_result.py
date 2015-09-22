from yowsup.layers.protocol_iq.protocolentities.iq_result import ResultIqProtocolEntity
from yowsup.structs.protocoltreenode import ProtocolTreeNode
class ResultLastseenIqProtocolEntity(ResultIqProtocolEntity):
    def __init__(self, jid, seconds, _id = None):
        super(ResultLastseenIqProtocolEntity, self).__init__(_from=jid, _id=_id)
        self.setSeconds(seconds)

    def setSeconds(self, seconds):
        self.seconds = int(seconds)

    def getSeconds(self):
        return self.seconds

    def __str__(self):
        out = super(ResultIqProtocolEntity, self).__str__()
        out += "Seconds: %s\n" % self.seconds
        return out

    def toProtocolTreeNode(self):
        node = super(ResultLastseenIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("query", {"seconds": str(self.seconds)}))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        return ResultLastseenIqProtocolEntity(node["from"], node.getChild("query")["seconds"], node["id"])