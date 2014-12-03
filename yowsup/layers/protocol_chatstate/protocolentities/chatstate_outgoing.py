from .chatstate import ChatstateProtocolEntity
class OutgoingChatstateProtocolEntity(ChatstateProtocolEntity):
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

    def __init__(self, _state, _to):
        super(OutgoingChatstateProtocolEntity, self).__init__(_state)
        self.setOutgoingData(_to)

    def setOutgoingData(self, _to):
        self._to = _to
    
    def toProtocolTreeNode(self):
        node = super(OutgoingChatstateProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("to", self._to)
        return node

    def __str__(self):
        out  = super(OutgoingChatstateProtocolEntity, self).__str__()
        out += "To: %s\n" % self._to
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = ChatstateProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = OutgoingChatstateProtocolEntity
        entity.setOutgoingData(
            node.getAttributeValue("to"),
        )
        return entity
