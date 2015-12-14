from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_notifications.protocolentities import NotificationProtocolEntity

class GroupsNotificationProtocolEntity(NotificationProtocolEntity):
    '''

    <notification notify="WhatsApp" id="{{id}}" t="1420402514" participant="{{participant_jiid}}" from="{{group_jid}}" type="w:gp2">
    </notification>

    '''

    def __init__(self, _id,  _from, timestamp, notify, participant, offline):
        super(GroupsNotificationProtocolEntity, self).__init__("w:gp2", _id, _from, timestamp, notify, offline)
        self.setParticipant(participant)
        self.setGroupId(_from)

    def setParticipant(self, participant):
        self._participant = participant

    def getParticipant(self, full = True):
        return self._participant if full else self._participant.split('@')[0]

    def getGroupId(self):
        return self.groupId

    def setGroupId(self, groupId):
        self.groupId = groupId


    def __str__(self):
        out = super(GroupsNotificationProtocolEntity, self).__str__()
        out += "Participant: %s\n" % self.getParticipant()
        return out

    def toProtocolTreeNode(self):
        node = super(GroupsNotificationProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("participant", self.getParticipant())
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = super(GroupsNotificationProtocolEntity, GroupsNotificationProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = GroupsNotificationProtocolEntity
        entity.setParticipant(node.getAttributeValue("participant"))
        entity.setGroupId(node.getAttributeValue("from"))
        return entity
