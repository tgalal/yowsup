from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_groups_participants import ParticipantsGroupsIqProtocolEntity

class ListParticipantsIqProtocolEntity(ParticipantsGroupsIqProtocolEntity):
    '''
    <iq type="get" id="{{id}}" xmlns="w:g2", to="{{group_jid}}">
        <list>
        </list>
    </iq>
    '''
    
    def __init__(self, group_jid, _id = None):
        super(ListParticipantsIqProtocolEntity, self).__init__(jid = group_jid, _id = _id, _type = "get", _mode="list")
    
    @staticmethod
    def fromProtocolTreeNode(node):
        entity = super(ListParticipantsIqProtocolEntity, ListParticipantsIqProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = ListParticipantsIqProtocolEntity
        participantList = []
        for participantNode in node.getChild("List").getAllChildren():
            participantList.append(participantNode["jid"])
        entity.setProps(node.getAttributeValue("to"), participantList)
        return entity
