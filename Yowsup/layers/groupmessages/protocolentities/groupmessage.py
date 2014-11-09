from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
from Yowsup.layers.messages.protocolentities import MessageProtocolEntity
class GroupMessageProtocolEntity(MessageProtocolEntity):
    '''
    <message participant="{{PARTICIPANT_JID}}" 
        t="{{TIME_STAMP}}" from="{{GROUP_JID}}" 
        offline="{{OFFLINE}}" type="{{MESSAGE_TYPE}}" id="{{MESSAGE_ID}}" notify="{{NOTIFY_NAME}}">
    </message>
    '''
    def __init__(self, _id, _from, participant, timestamp, notify, offline, retry = None):
        super(GroupMessageProtocolEntity, self).__init__("text", _id, _from, timestamp, notify, offline, retry)
        self.setParitipant(participant)

    def __str__(self):
        out  = super(GroupMessageProtocolEntity, self).__str__()
        out += "participant: %s\n" % self.participant
        return out

    def setParticipant(self, participant):
        self.participant = participant

    def toProtocolTreeNode(self):
        node = super(GroupMessageProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("participant", self.participant)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = MessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = GroupMessageProtocolEntity
        entity.setParticipant(node.getAttributeValue("participant"))
        return entity
