from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_notifications.protocolentities import NotificationProtocolEntity
from .notification_groups import GroupsNotificationProtocolEntity

class SubjectGroupsNotificationProtocolEntity(GroupsNotificationProtocolEntity):
    '''

    <notification notify="WhatsApp" id="{{id}}" t="{{TIMESTAMP}}" participant="{{PARTICIPANT_JID}}" from="{{GROUP_JID}}" type="w:gp2">
        <subject s_t="{{subject_set_timestamp}}" s_o="{{subject_owner_jid}}" subject="{{SUBJECT}}">
        </subject>
    </notification>

    '''

    def __init__(self, _type, _id,  _from, timestamp, notify, participant, subject):
        super(SubjectGroupsNotificationProtocolEntity, self).__init__(_id, _from, timestamp, notify, participant)
        self.setSubjectData(subject)

    def setSubjectData(self, subject, subjectOwner, subjectTimestamp):
        self.subject = subject
        self.subjectOwner = subjectOwner
        self.subjectTimestamp = int(subjectTimestamp)

    def getSubject(self):
        return self.subject

    def getSubjectOwner(self, full = True):
        return self.subjectOwner if full else self.subjectOwner.split('@')[0]

    def getSubjectTimestamp(self):
        return self.subjectTimestamp

    def __str__(self):
        out = super(SubjectGroupsNotificationProtocolEntity, self).__str__()
        out += "New subject: %s\n" % self.getSubject()
        out += "Set by: %s\n" % self.getSubjectOwner()
        return out

    def toProtocolTreeNode(self):
        node = super(SubjectGroupsNotificationProtocolEntity, self).toProtocolTreeNode()
        subjectNode = ProtocolTreeNode("subject", {
            "s_t": str(self.getSubjectTimestamp()),
            "s_o": self.getSubjectOwner(),
            "subject": self.getSubject()
        })
        node.addChild(subjectNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = super(SubjectGroupsNotificationProtocolEntity, SubjectGroupsNotificationProtocolEntity).fromProtocolTreeNode(node)
        entity.__class__ = SubjectGroupsNotificationProtocolEntity
        subjectNode = node.getChild("subject")
        entity.setSubjectData(subjectNode["subject"], subjectNode["s_o"], subjectNode["s_t"])
        return entity
