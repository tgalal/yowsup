from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import IqProtocolEntity
class CleanIqProtocolEntity(IqProtocolEntity):
    '''
    <iq id="" type="set" to="self.domain" xmlns="urn:xmpp:whatsapp:dirty">
        <clean type="{{dirty_type}}"></clean>
    </iq>
    '''
    def __init__(self, cleanType, to, _id = None):
        super(CleanIqProtocolEntity, self).__init__(
            "urn:xmpp:whatsapp:dirty",
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
        node = super(CleanIqProtocolEntity, self).toProtocolTreeNode()
        cleanNode = ProtocolTreeNode("clean", {"type": self.cleanType})
        node.addChild(cleanNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = IqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = CleanIqProtocolEntity
        entity.setProps(node.getChild("clean").getAttributeValue("type"))
        return entity