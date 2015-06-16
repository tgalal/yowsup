from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_groups_participants import ParticipantsGroupsIqProtocolEntity

class RemoveParticipantsIqProtocolEntity(ParticipantsGroupsIqProtocolEntity):
    '''
    <iq type="set" id="{{id}}" xmlns="w:g2", to="{{group_jid}}">
        <remove>
            <participant jid="{{jid}}"></participant>
            <participant jid="{{jid}}"></participant>
        </remove>
    </iq>
    '''
    
    def __init__(self, group_jid, participantList, _id = None):
        super(RemoveParticipantsIqProtocolEntity, self).__init__(jid = group_jid, _id = _id, _type = "set", _mode="remove", _participantList = participantList)
        
    @staticmethod
    def fromProtocolTreeNode(node):
        entity = super(RemoveParticipantsIqProtocolEntity, RemoveParticipantsIqProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = RemoveParticipantsIqProtocolEntity
        participantList = []
        for participantNode in node.getChild("remove").getAllChildren():
            participantList.append(participantNode["jid"])
        entity.setProps(node.getAttributeValue("to"), participantList)
        return entity
