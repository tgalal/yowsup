from .chatstate import ChatstateProtocolEntity
class IncomingChatstateProtocolEntity(ChatstateProtocolEntity):
    '''
    INCOMING

    <chatstate from="xxxxxxxxxxx@s.whatsapp.net">
    <{{composing|paused}}></{{composing|paused}}>
    </chatstate>

    OUTGOING

    <chatstate to="xxxxxxxxxxx@s.whatsapp.net">
    <{{composing|paused}}></{{composing|paused}}>
    </chatstate>
    '''

    def __init__(self, _state, _from):
        super(IncomingChatstateProtocolEntity, self).__init__(_state)
        self.setIncomingData(_from)

    def setIncomingData(self, _from):
        self._from = _from
    
    def toProtocolTreeNode(self):
        node = super(IncomingChatstateProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("from", self._from)
        return node

    def __str__(self):
        out  = super(IncomingChatstateProtocolEntity, self).__str__()
        out += "From: %s\n" % self._from
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = ChatstateProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = IncomingChatstateProtocolEntity
        entity.setIncomingData(
            node.getAttributeValue("from"),
        )
        return entity
