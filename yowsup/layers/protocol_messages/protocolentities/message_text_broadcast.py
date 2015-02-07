from .message_text import TextMessageProtocolEntity
from yowsup.structs import ProtocolTreeNode
import time
class BroadcastTextMessage(TextMessageProtocolEntity):
    schema = (__file__, "schemas/message_text_broadcast.xsd")
    def __init__(self, jids, body, _id = None, broadcastTime = None):
        broadcastTime = int(broadcastTime) or int(time.time() * 1000)
        super(BroadcastTextMessage, self).__init__(body, to = "%s@broadcast" % broadcastTime, _id = _id)
        self.setBroadcastProps(jids)

    def setBroadcastProps(self, jids):
        assert type(jids) is list, "jids must be a list, got %s instead." % type(jids)
        self.jids = jids

    def toProtocolTreeNode(self):
        node = super(BroadcastTextMessage, self).toProtocolTreeNode()
        toNodes = [ProtocolTreeNode("to", {"jid": jid}) for jid in self.jids]
        broadcastNode = ProtocolTreeNode("broadcast", children = toNodes)
        node.addChild(broadcastNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        jids = [toNode.getAttributeValue("jid") for toNode in node.getChild("broadcast").getAllChildren()]
        entity = BroadcastTextMessage(jids, node.getChild("body").getData(), node["id"], node["to"].split('@')[0])
        return entity
