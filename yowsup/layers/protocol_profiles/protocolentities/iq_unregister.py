from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
from yowsup.structs import ProtocolTreeNode

class UnregisterIqProtocolEntity(IqProtocolEntity):
    schema = (__file__, "schemas/iq_unregister.xsd")
    """
    <iq id="1234" type="get" to="s.whatsapp.net">
        <remove xmlns="urn:xmpp:whatsapp:account" />
    </iq>
    """

    XMLNS = "urn:xmpp:whatsapp:account"

    def __init__(self, _id = None):
        super(UnregisterIqProtocolEntity, self).__init__(_type = "get", to = "s.whatsapp.net", _id = _id)

    def toProtocolTreeNode(self):
        node = super(UnregisterIqProtocolEntity, self).toProtocolTreeNode()
        rmNode = ProtocolTreeNode("remove", {"xmlns": self.__class__.XMLNS})
        node.addChild(rmNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = UnregisterIqProtocolEntity(node["id"])
        return entity