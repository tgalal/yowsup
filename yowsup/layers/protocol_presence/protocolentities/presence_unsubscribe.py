from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .presence import PresenceProtocolEntity
class UnsubscribePresenceProtocolEntity(PresenceProtocolEntity):

    '''
    <presence type="unsubscribe" to="jid"></presence>
    '''

    def __init__(self, jid):
        super(UnsubscribePresenceProtocolEntity, self).__init__("unsubscribe")
        self.setProps(jid)

    def setProps(self, jid):
        self.jid = jid
    
    def toProtocolTreeNode(self):
        node = super(UnsubscribePresenceProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("to", self.jid)
        return node

    def __str__(self):
        out  = super(UnsubscribePresenceProtocolEntity, self).__str__()
        out += "To: %s\n" % self.jid
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = PresenceProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = UnsubscribePresenceProtocolEntity
        entity.setProps(
            node.getAttributeValue("to")
        )
        return entity
