from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_groups import GroupsIqProtocolEntity


class AddParticipantsIqProtocolEntity(GroupsIqProtocolEntity):
    '''
    <iq type="set" id="{{id}}" xmlns="w:g", to="{{group_jid}}">
        <add>
            <participant jid="{{jid}}"></participant>
            <participant jid="{{jid}}"></participant>
        </add>
    </iq>
    '''

    def __init__(self, group_jid, participantList, _id = None):
        super(AddParticipantsIqProtocolEntity, self).__init__(to = group_jid, _id = _id, _type = "set")
        self.setProps(group_jid, participantList)

    def setProps(self, group_jid, participantList):
        assert type(participantList) is list, "Must be a list of jids, got %s instead." % type(participantList)
        assert len(participantList), "Participant list cannot be empty"
        self.group_jid = group_jid
        self.participantList = participantList

    def toProtocolTreeNode(self):
        node = super(AddParticipantsIqProtocolEntity, self).toProtocolTreeNode()
        participantNodes = [
            ProtocolTreeNode("participant", {
                "jid":       participant
            })
            for participant in self.participantList
        ]
        node.addChild(ProtocolTreeNode("add",{}, participantNodes))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = GroupsIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = AddParticipantsIqProtocolEntity
        participantList = []
        for participantNode in node.getChild("add").node.getAllChildren():
            participantList.append(participantNode["jid"])
        entity.setProps(node.getAttributeValue("to"), participantList)
        return entity
