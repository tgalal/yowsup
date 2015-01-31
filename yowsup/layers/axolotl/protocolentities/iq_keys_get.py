from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode
class GetKeysIqProtocolEntity(IqProtocolEntity):
    schema = (__file__, "schemas/iq_keys_get.xsd")
    def __init__(self, jids, _id  = None):
        super(GetKeysIqProtocolEntity, self).__init__(_type = "get", to = "s.whatsapp.net", _id = _id)
        self.setJids(jids)

    def setJids(self, jids):
        assert type(jids) is list, "expected list of jids, got %s" % type(jids)
        self.jids = jids

    def getJids(self):
        return self.jids

    def toProtocolTreeNode(self):
        node = super(GetKeysIqProtocolEntity, self).getProtocolTreeNode("encrypt")
        keyNode = ProtocolTreeNode("key", parent=node)

        for jid in self.getJids():
            ProtocolTreeNode("user", { "jid": jid }, ns=(None, "encrypt"), parent=keyNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        userNodes = node.getChild("key").getAllChildren()
        jids = [unode["jid"] for unode in userNodes]
        return GetKeysIqProtocolEntity(jids, node["id"])
