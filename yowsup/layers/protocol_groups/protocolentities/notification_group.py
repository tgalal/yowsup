from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_notifications.protocolentities import NotificationProtocolEntity

class GroupNotificationProtocolEntity(NotificationProtocolEntity):
    '''

    <notification notify="WhatsApp" id="{{id}}" t="1420402514" participant="{{participant_jiid}}" from="{{group_jid}}" type="w:gp2">
    </notification>

    '''

    def __init__(self, _id,  _from, timestamp, notify, participant, offline):
        super(GroupNotificationProtocolEntity, self).__init__("w:gp2", _id, _from, timestamp, notify, offline)
        self.setParticipant(participant)

    def setParticipant(self, participant):
        self._participant = participant

    def getParticipant(self, full = True):
        return self._participant if full else self._participant.split('@')[0]

    def __str__(self):
        out = super(GroupNotificationProtocolEntity, self).__str__()
        out += "Participant: %s\n" % self.getParticipant()
        return out

    def toProtocolTreeNode(self):
        node = super(GroupNotificationProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("participant", self.getParticipant())
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = NotificationProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = GroupNotificationProtocolEntity
        entity.setParticipant(node.getAttributeValue("participant"))
        return entity