from .message_text import TextMessageProtocolEntity
from yowsup.structs import ProtocolTreeNode
class BroadcastTextMessage(TextMessageProtocolEntity):
    def __init__(self, jids, body):
        super(BroadcastTextMessage, self).__init__(body, to = "broadcast")
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
        entity = TextMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = BroadcastTextMessage
        jids = [toNode.getAttributeValue("jid") for toNode in node.getChild("broadcast").getAllChildren()]
        entity.setBroadcastProps(jids)
        return entity
