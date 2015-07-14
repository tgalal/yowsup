from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode

class UnregisterIqProtocolEntity(IqProtocolEntity):

    XMLNS = "urn:xmpp:whatsapp:account"

    def __init__(self):
        super(UnregisterIqProtocolEntity, self).__init__(_type = "get", to = "s.whatsapp.net")

    def toProtocolTreeNode(self):
        node = super(UnregisterIqProtocolEntity, self).toProtocolTreeNode()
        rmNode = ProtocolTreeNode("remove", {"xmlns": self.__class__.XMLNS})
        node.addChild(rmNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = IqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = UnregisterIqProtocolEntity
        removeNode = node.getChild("remove")
        assert removeNode["xmlns"] == UnregisterIqProtocolEntity.XMLNS, "Not an account delete xmlns, got %s" % removeNode["xmlns"]

        return entity