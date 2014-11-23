from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .ack import AckProtocolEntity
class OutgoingAckProtocolEntity(AckProtocolEntity):

    '''
    <ack type="{{delivery | ?}}" class="{{message | receipt | ?}}" id="{{MESSAGE_ID}}">
    </ack>
    '''

    def __init__(self, _id, _class, _type):
        super(OutgoingAckProtocolEntity, self).__init__(_id, _class)
        self.setOutgoingData(_type)

    def setOutgoingData(self, _type):
        self._type = _type
    
    def toProtocolTreeNode(self):
        node = super(OutgoingAckProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("type", self._type)
        return node

    def __str__(self):
        out  = super(OutgoingAckProtocolEntity, self).__str__()
        out += "Type: %s\n" % self._type
        return out

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = AckProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = OutgoingAckProtocolEntity
        entity.setOutgoingData(
            node.getAttributeValue("type")
        )
        return entity
