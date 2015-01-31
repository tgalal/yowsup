from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
class CleanIqProtocolEntity(IqProtocolEntity):
    '''
    <iq id="" type="set" to="self.domain" xmlns="urn:xmpp:whatsapp:dirty">
        <clean type="{{dirty_type}}"></clean>
    </iq>
    '''

    schema = (__file__, "schemas/clean_iq.xsd")

    def __init__(self, cleanType, to, _id = None):
        super(CleanIqProtocolEntity, self).__init__(
            _id = _id,
            _type = "set",
            to = to
        )
        self.setProps(cleanType)

    def setProps(self, cleanType):
        self.cleanType = cleanType

    def __str__(self):
        out = super(CleanIqProtocolEntity, self).__str__()
        out += "Clean Type: %s\n" % self.cleanType
        return out

    def toProtocolTreeNode(self):
        node = super(CleanIqProtocolEntity, self).getProtocolTreeNode("urn:xmpp:whatsapp:dirty")
        cleanNode = ProtocolTreeNode("clean", {"type": self.cleanType}, ns = "urn:xmpp:whatsapp:dirty")
        node.addChild(cleanNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = CleanIqProtocolEntity(node.getChild("clean")["type"], node["to"], _id=node["id"])
        return entity