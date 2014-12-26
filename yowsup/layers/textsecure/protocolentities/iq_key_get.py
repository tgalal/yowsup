from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode
class GetKeysIqProtocolEntity(IqProtocolEntity):
    def __init__(self, jid):
        super(GetKeysIqProtocolEntity, self).__init__("encrypt", _type = "get", to = "s.whatsapp.net")
        self.setJid(jid)

    def setJid(self, jid):
        self.jid = jid

    def toProtocolTreeNode(self):
        node = super(GetKeysIqProtocolEntity, self).toProtocolTreeNode()
        keyNode = ProtocolTreeNode("key")
        userNode = ProtocolTreeNode("user", { "jid": self.jid })
        keyNode.addChild(userNode)
        node.addChild(keyNode)
        return node