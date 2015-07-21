from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_groups_participants import ParticipantsGroupsIqProtocolEntity

class AddParticipantsIqProtocolEntity(ParticipantsGroupsIqProtocolEntity):
    '''
    <iq type="set" id="{{id}}" xmlns="w:g2", to="{{group_jid}}">
        <add>
            <participant jid="{{jid}}"></participant>
            <participant jid="{{jid}}"></participant>
        </add>
    </iq>
    '''

    def __init__(self, group_jid, participantList, _id = None):
        super(AddParticipantsIqProtocolEntity, self).__init__(group_jid, participantList, "add", _id = _id)

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = super(AddParticipantsIqProtocolEntity, AddParticipantsIqProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = AddParticipantsIqProtocolEntity
        participantList = []
        for participantNode in node.getChild("add").getAllChildren():
            participantList.append(participantNode["jid"])
        entity.setProps(node.getAttributeValue("to"), participantList)
        return entity
