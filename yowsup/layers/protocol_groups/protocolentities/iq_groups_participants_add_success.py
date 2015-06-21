from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import ResultIqProtocolEntity
class SuccessAddParticipantsIqProtocolEntity(ResultIqProtocolEntity):
    '''
    <iq type="result" from="{{group_jid}}" id="{{id}}">
        <add type="success" participant="{{jid}}"></add>
        <add type="success" participant="{{jid}}"></add>
    </iq>
    '''

    def __init__(self, _id, groupId, participantList):
        super(SuccessAddParticipantsIqProtocolEntity, self).__init__(_from = groupId, _id = _id)
        self.setProps(groupId, participantList)

    def setProps(self, groupId, participantList):
        self.groupId = groupId
        self.participantList = participantList
        self.action = 'add'

    def getAction(self):
        return self.action

    def toProtocolTreeNode(self):
        node = super(SuccessAddParticipantsIqProtocolEntity, self).toProtocolTreeNode()
        participantNodes = [
            ProtocolTreeNode("add", {
                "type":                     "success",
                "participant":       participant
            })
            for participant in self.participantList
        ]
        node.addChildren(participantNodes)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = super(SuccessAddParticipantsIqProtocolEntity, SuccessAddParticipantsIqProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = SuccessAddParticipantsIqProtocolEntity
        participantList = []
        for participantNode in node.getAllChildren():
            if participantNode["type"]=="success":
                participantList.append(participantNode["participant"])
        entity.setProps(node.getAttributeValue("from"), participantList)
        return entity
