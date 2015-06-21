from .notification_groups import GroupsNotificationProtocolEntity
from yowsup.structs import ProtocolTreeNode
class RemoveGroupsNotificationProtocolEntity(GroupsNotificationProtocolEntity):
    '''
<notification notify="{{NOTIFY_NAME}}" id="{{id}}" t="{{TIMESTAMP}}" participant="{{participant_jiid}}" from="{{group_jid}}" type="w:gp2">
<remove subject="{{GROUPSUBJ}}">
<participant jid="{{participant_jiid}}">
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

        assert type(participants) is dict, "Participants must be a dict {jid => type?}"

        self.subject = subject
        self.participants = participants

    def getParticipants(self):
        return self.participants

    def getSubject(self):
        return self.subject

    def toProtocolTreeNode(self):
        node = super(RemoveGroupsNotificationProtocolEntity, self).toProtocolTreeNode()
        createNode = ProtocolTreeNode("remove", {"subject": self.getSubject()})
        participants = []
        for jid, _type in self.getParticipants().items():
            pnode = ProtocolTreeNode("participant", {"jid": jid})
            participants.append(pnode)

        createNode.addChildren(participants)
        node.addChild(createNode)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        createNode = node.getChild("remove")
        participants = {}
        for p in createNode.getAllChildren("participant"):
            participants[p["jid"]] = p["type"]

        return RemoveGroupsNotificationProtocolEntity(
            node["id"], node["from"], node["t"], node["notify"], node["participant"], node["offline"],
            createNode["subject"], participants
        )
