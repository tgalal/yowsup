from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_groups import GroupsIqProtocolEntity
class RemoveParticipantsIqProtocolEntity(GroupsIqProtocolEntity):
    '''
    <iq type="set" id="{{id}}" xmlns="w:g", to="{{group_jid}}">
        <remove>
            <participant jid="{{jid}}""></participant>
            <participant jid="{{jid}}""></participant>
        </remove>
    </iq>
    '''

    def __init__(self, jid, participantList, _id = None):
        super(RemoveParticipantsIqProtocolEntity, self).__init__(to = jid, _id = _id, _type = "set")
        self.setProps(participantList)

    def setProps(self, participantList):
        assert type(participantList) is list, "Must be a list of jids, got %s instead." % type(participantList)
        assert len(participantList), "Participant list cannot be empty"
        self.participantList = participantList

    def toProtocolTreeNode(self):
        node = super(RemoveParticipantsIqProtocolEntity, self).toProtocolTreeNode()

        participantNodes = [
            ProtocolTreeNode("participant", {
                "jid":       participant
            })
            for participant in self.participantList
        ]
        node.addChild(ProtocolTreeNode("remove",{}, participantNodes))
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = GroupsIqProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = RemoveParticipantsIqProtocolEntity
        #entity.setProps(node.getChild("group").getAttributeValue("subject"))
        return entity
