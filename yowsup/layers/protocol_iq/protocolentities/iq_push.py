from .iq import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode
class PushIqProtocolEntity(IqProtocolEntity):
    def __init__(self):
        super(PushIqProtocolEntity, self).__init__("urn:xmpp:whatsapp:push", _type="get")

    def toProtocolTreeNode(self):
        node = super(PushIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("config"))
        return node