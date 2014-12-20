from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode
class PrivacyListIqProtocolEntity(IqProtocolEntity):
    def __init__(self, name = "default"):
        super(PrivacyListIqProtocolEntity, self).__init__("jabber:iq:privacy", _type="get")
        self.setListName(name)

    def setListName(self, name):
        self.listName = name

    def toProtocolTreeNode(self):
        node = super(PrivacyListIqProtocolEntity, self).toProtocolTreeNode()
        queryNode = ProtocolTreeNode("query")
        listNode = ProtocolTreeNode("list", {"name": self.listName})
        queryNode.addChild(listNode)
        node.addChild(queryNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = IqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = PrivacyListIqProtocolEntity
        entity.setListName(node.getChild("query").getChild("list")["name"])
        return entity
