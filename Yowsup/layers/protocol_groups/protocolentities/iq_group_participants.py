from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_group import GroupIqProtocolEntity
class ParticipantsGroupIqProtocolEntity(GroupIqProtocolEntity):
    '''
    <iq type="get" id="{{id}}" xmlns="w:g", to={{group_jid}}">
        <list></list>
    </iq>
    '''
    def __init__(self, jid, _id = None):
        super(ParticipantsGroupIqProtocolEntity, self).__init__(_to = jid, _id = _id, _type = "get")

    def toProtocolTreeNode(self):
        node = super(ParticipantsGroupIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("list",{}))

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = GroupIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = ParticipantsGroupIqProtocolEntity
