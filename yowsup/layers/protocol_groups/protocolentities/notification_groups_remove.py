from .notification_groups import GroupsNotificationProtocolEntity
from yowsup.structs import ProtocolTreeNode
class RemoveGroupsNotificationProtocolEntity(GroupsNotificationProtocolEntity):
    '''
<notification notify="{{NOTIFY_NAME}}" id="{{id}}" t="{{TIMESTAMP}}" participant="{{participant_jiid}}" from="{{group_jid}}" type="w:gp2" mode="none">
<remove subject="{{subject}}">
<participant jid="{{participant_jid}}">
</participant>
</remove>
</notification>
    '''
    TYPE_PARTICIPANT_ADMIN = "admin"
    def __init__(self, _id, _from, timestamp, notify, participant, offline,
                 subject,
                 participants):
        super(RemoveGroupsNotificationProtocolEntity, self).__init__(_id, _from, timestamp, notify, participant, offline)
        self.setGroupProps(subject, participants)

    def setGroupProps(self,
                      subject,
                      participants):

        assert type(participants) is list, "Must be a list of jids, got %s instead." % type(participants)

        self.subject = subject
        self.participants = participants

    def getParticipants(self):
        return self.participants

    def getSubject(self):
        return self.subject

    def toProtocolTreeNode(self):
        node = super(RemoveGroupsNotificationProtocolEntity, self).toProtocolTreeNode()
        removeNode = ProtocolTreeNode("remove", {"subject": self.subject})
        participants = []
        for jid in self.getParticipants():
            pnode = ProtocolTreeNode("participant", {"jid": jid})
            participants.append(pnode)

        removeNode.addChildren(participants)
        node.addChild(removeNode)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        removeNode = node.getChild("remove")
        participants = []
        for p in removeNode.getAllChildren("participant"):
            participants.append(p["jid"])

        return RemoveGroupsNotificationProtocolEntity(
            node["id"], node["from"], node["t"], node["notify"], node["participant"], node["offline"],
            removeNode["subject"], participants
        )
