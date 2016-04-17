from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .ack import AckProtocolEntity
class OutgoingAckProtocolEntity(AckProtocolEntity):

    '''
    <ack type="{{delivery | read}}" class="{{message | receipt | ?}}" id="{{MESSAGE_ID}} to={{TO_JID}}">
    </ack>

    <ack to="{{GROUP_JID}}" participant="{{JID}}" id="{{MESSAGE_ID}}" class="receipt" type="{{read | }}">
    </ack>

    '''

    def __init__(self, _id, _class, _type, to, participant = None):
        super(OutgoingAckProtocolEntity, self).__init__(_id, _class)
        self.setOutgoingData(_type, to, participant)

    def setOutgoingData(self, _type, _to, _participant):
        self._type = _type
        self._to = _to
        self._participant = _participant

    def toProtocolTreeNode(self):
        node = super(OutgoingAckProtocolEntity, self).toProtocolTreeNode()
        if self._type:
            node.setAttribute("type", self._type)
        node.setAttribute("to", self._to)
        if self._participant:
            node.setAttribute("participant", self._participant)
        return node

    def __str__(self):
        out  = super(OutgoingAckProtocolEntity, self).__str__()
        out += "Type: %s\n" % self._type
        out += "To: %s\n" % self._to
        if self._participant:
            out += "Participant: %s\n" % self._participant
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = AckProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = OutgoingAckProtocolEntity
        entity.setOutgoingData(
            node.getAttributeValue("type"),
            node.getAttributeValue("to"),
            node.getAttributeValue("participant")
        )
        return entity
