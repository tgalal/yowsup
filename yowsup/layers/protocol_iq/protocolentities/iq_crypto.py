from .iq import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode
class CryptoIqProtocolEntity(IqProtocolEntity):
    def __init__(self):
        super(CryptoIqProtocolEntity, self).__init__("urn:xmpp:whatsapp:account", _type="get")

    def toProtocolTreeNode(self):
        node = super(CryptoIqProtocolEntity, self).toProtocolTreeNode()
        cryptoNode = ProtocolTreeNode("crypto", {"action": "create"})
        googleNode = ProtocolTreeNode("google", data = "fe5cf90c511fb899781bbed754577098e460d048312c8b36c11c91ca4b49ca34".decode('hex'))
        cryptoNode.addChild(googleNode)
        node.addChild(cryptoNode)
        return node