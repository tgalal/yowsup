from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_groups import GroupsIqProtocolEntity
class ParticipantsGroupsIqProtocolEntity(GroupsIqProtocolEntity):
    '''
    <iq type="get" id="{{id}}" xmlns="w:g", to={{group_jid}}">
        <list></list>
    </iq>
    '''
    def __init__(self, jid, _id = None):
        super(ParticipantsGroupsIqProtocolEntity, self).__init__(to = jid, _id = _id, _type = "get")

    def toProtocolTreeNode(self):
        node = super(ParticipantsGroupsIqProtocolEntity, self).toProtocolTreeNode()
        node.addChild(ProtocolTreeNode("list",{}))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = GroupsIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = ParticipantsGroupsIqProtocolEntity
        return entity
