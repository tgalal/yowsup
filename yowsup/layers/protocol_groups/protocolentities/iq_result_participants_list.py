from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import ResultIqProtocolEntity
class ListParticipantsResultIqProtocolEntity(ResultIqProtocolEntity):
    '''
    <iq type="result" from="{{GROUP_ID}}" id="{{IQ_ID}}">
        <participant jid="{{PARTICIPANT_JID}}">
        </participant>
    </iq>
    '''

    def __init__(self, _from, participantList):
        super(ListParticipantsResultIqProtocolEntity, self).__init__(_from = _from)
        self.setParticipants(participantList)

    def __str__(self):
        out = super(ListParticipantsResultIqProtocolEntity, self).__str__()
        out += "Participants: %s\n" % " ".join(self.participantList)
        return out

    def getParticipants(self):
        return self.participantList

    def setParticipants(self, participants):
        self.participantList = participants

    def toProtocolTreeNode(self):
        node = super(ListParticipantsResultIqProtocolEntity, self).toProtocolTreeNode()

        participantNodes = [
            ProtocolTreeNode("participant", {
                "jid":       participant
            })
            for participant in self.participantList
        ]

        node.addChildren(participantNodes)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = super(ListParticipantsResultIqProtocolEntity, ListParticipantsResultIqProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = ListParticipantsResultIqProtocolEntity
        entity.setParticipants([ pNode.getAttributeValue("jid") for pNode in node.getAllChildren() ])
        return entity
