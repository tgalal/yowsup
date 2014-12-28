from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_notifications.protocolentities import NotificationProtocolEntity

class GroupNotificationProtocolEntity(NotificationProtocolEntity):
    '''

    <notification participant="{{SENDER_JID}}" t="{{TIMESTAMP}}" from="{{GROUP_JID}}" type="{{TYPE}}" id="{{NOTIFICATION_ID}}" notify="{{NOTIFY_NAME}}">
        {{CONTENTS}}
    </notification>

    '''

    def __init__(self, _type, _id,  _from, timestamp, notify, participant):
        super(SubjectNotificationProtocolEntity, self).__init__(_type, _id, _from, timestamp, notify, False)
        self.setParticipant(participant)

    def setParticipant(self, participant):
        self._participant = participant

    def getParticipant(self):
        return self._participant

    def toProtocolTreeNode(self):
        node = super(SubjectNotificationProtocolEntity, self).toProtocolTreeNode()
        node.setAttribute("participant", self.getParticipant())
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = NotificationProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = GroupNotificationProtocolEntity
        entity.setParticipant(node.getAttributeValue("participant"))
        return entity