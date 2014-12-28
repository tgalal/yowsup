from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_notifications.protocolentities import NotificationProtocolEntity
from .notification_group import GroupNotificationProtocolEntity

class SubjectNotificationProtocolEntity(GroupNotificationProtocolEntity):
    '''

    <notification participant="{{SENDER_JID}}" t="{{TIMESTAMP}}" from="{{GROUP_JID}}" type="subject" id="{{NOTIFICATION_ID}}" notify="{{NOTIFY_NAME}}">
        <body>{{SUBJECT}}</body>
    </notification>

    '''

    def __init__(self, _type, _id,  _from, timestamp, notify, participant, subject):
        super(SubjectNotificationProtocolEntity, self).__init__("subject", _id, _from, timestamp, notify, participant)
        self.setSubject(subject)

    def setSubject(self, subject):
        self.subject = subject

    def getSubject(self):
        return self.subject

    def toProtocolTreeNode(self):
        node = super(SubjectNotificationProtocolEntity, self).toProtocolTreeNode()
        bodyNode = ProtocolTreeNode("body", {}, None, self.subject)
        node.addChild(setNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = GroupNotificationProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = SubjectNotificationProtocolEntity
        entity.setSubject(node.getChild("body").getData())
        return entity