from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .presence import PresenceProtocolEntity
class SubscribePresenceProtocolEntity(PresenceProtocolEntity):

    '''
    <presence type="subscribe" to="jid"></presence>
    '''

    def __init__(self, jid):
        super(SubscribePresenceProtocolEntity, self).__init__("subscribe")
        self.setProps(jid)

    def setProps(self, jid):
        self.jid = jid
    
    def toProtocolTreeNode(self):
        node = super(SubscribePresenceProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("to", self.jid)
        return node

    def __str__(self):
        out  = super(SubscribePresenceProtocolEntity, self).__str__()
        out += "To: %s\n" % self.jid
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = PresenceProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = SubscribePresenceProtocolEntity
        entity.setProps(
            node.getAttributeValue("to")
        )
        return entity
