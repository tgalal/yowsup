from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .ack import AckProtocolEntity
class OutgoingAckProtocolEntity(AckProtocolEntity):

    '''
    <ack type="{{delivery | read}}" class="{{message | receipt | ?}}" id="{{MESSAGE_ID}} to={{TO_JID}}">
    </ack>
    '''

    def __init__(self, _id, _class, _type, _to):
        super(OutgoingAckProtocolEntity, self).__init__(_id, _class)
        self.setOutgoingData(_type, _to)

    def setOutgoingData(self, _type, _to):
        self._type = _type
        self._to = _to
    
    def toProtocolTreeNode(self):
        node = super(OutgoingAckProtocolEntity, self).toProtocolTreeNode()
        if self._type:
            node.setAttribute("type", self._type)
        node.setAttribute("to", self._to)
        return node

    def __str__(self):
        out  = super(OutgoingAckProtocolEntity, self).__str__()
        out += "Type: %s\n" % self._type
        out += "To: %s\n" % self._to
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = AckProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = OutgoingAckProtocolEntity
        entity.setOutgoingData(
            node.getAttributeValue("type"),
            node.getAttributeValue("to")
        )
        return entity
