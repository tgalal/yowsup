from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_groups_participants  import ParticipantsGroupsIqProtocolEntity

class DemoteParticipantsIqProtocolEntity(ParticipantsGroupsIqProtocolEntity):
    '''
    <iq type="set" id="{{id}}" xmlns="w:g2", to="{{group_jid}}">
        <demote>
            <participant jid="{{jid}}"></participant>
            <participant jid="{{jid}}"></participant>
        </demote>
    </iq>
    '''

    def __init__(self, group_jid, participantList, _id = None):
        super(DemoteParticipantsIqProtocolEntity, self).__init__(group_jid, participantList, "demote", _id = _id)
    
    @staticmethod
    def fromProtocolTreeNode(node):
        entity = super(DemoteParticipantsIqProtocolEntity, DemoteParticipantsIqProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = DemoteParticipantsIqProtocolEntity
        participantList = []
        for participantNode in node.getChild("demote").getAllChildren():
            participantList.append(participantNode["jid"])
        entity.setProps(node.getAttributeValue("to"), participantList)
        return entity
