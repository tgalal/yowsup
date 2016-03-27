from yowsup.common import YowConstants
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode
class GetKeysIqProtocolEntity(IqProtocolEntity):
    def __init__(self, jids):
        super(GetKeysIqProtocolEntity, self).__init__("encrypt", _type = "get", to = YowConstants.WHATSAPP_SERVER)
        self.setJids(jids)

    def setJids(self, jids):
        assert type(jids) is list, "expected list of jids, got %s" % type(jids)
        self.jids = jids

    def getJids(self):
        return self.jids

    def toProtocolTreeNode(self):
        node = super(GetKeysIqProtocolEntity, self).toProtocolTreeNode()
        keyNode = ProtocolTreeNode("key")

        for jid in self.getJids():
            userNode = ProtocolTreeNode("user", { "jid": jid })
            keyNode.addChild(userNode)
        node.addChild(keyNode)
        return node
