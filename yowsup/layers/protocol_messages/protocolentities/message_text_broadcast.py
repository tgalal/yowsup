from yowsup.common import YowConstants
from .message_text import TextMessageProtocolEntity
from yowsup.structs import ProtocolTreeNode
import time
class BroadcastTextMessage(TextMessageProtocolEntity):
    def __init__(self, jids, body):
        broadcastTime = int(time.time() * 1000)
        super(BroadcastTextMessage, self).__init__(body, to = "%s@%s" % (broadcastTime,YowConstants.WHATSAPP_BROADCAST_SERVER))
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
