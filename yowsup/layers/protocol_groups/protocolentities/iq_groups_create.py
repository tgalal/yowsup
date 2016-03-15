from yowsup.common import YowConstants
from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .iq_groups import GroupsIqProtocolEntity
class CreateGroupsIqProtocolEntity(GroupsIqProtocolEntity):
    '''
    <iq type="set" id="{{id}}" xmlns="w:g2", to="g.us">
        <create subject="{{subject}}">
             <participant jid="{{jid}}"></participant>
        </create>
    </iq>
    '''

    def __init__(self, subject, _id = None, participants = None):
        super(CreateGroupsIqProtocolEntity, self).__init__(to = YowConstants.WHATSAPP_GROUP_SERVER, _id = _id, _type = "set")
        self.setProps(subject)
        self.setParticipants(participants or [])

    def setProps(self, subject):
        self.subject = subject

    def setParticipants(self, participants):
        self.participantList = participants

    def toProtocolTreeNode(self):
        node = super(CreateGroupsIqProtocolEntity, self).toProtocolTreeNode()
        cnode = ProtocolTreeNode("create",{ "subject": self.subject})
        participantNodes = [
            ProtocolTreeNode("participant", {
                "jid":       participant
            })
            for participant in self.participantList
        ]
        cnode.addChildren(participantNodes)
        node.addChild(cnode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = super(CreateGroupsIqProtocolEntity,CreateGroupsIqProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = CreateGroupsIqProtocolEntity
        entity.setProps(node.getChild("create").getAttributeValue("subject"))
        participantList = []
        for participantNode in node.getChild("create").getAllChildren():
            participantList.append(participantNode["jid"])
        entity.setParticipants(participantList)
        return entity
