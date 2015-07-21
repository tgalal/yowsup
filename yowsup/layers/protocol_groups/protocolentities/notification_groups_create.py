from .notification_groups import GroupsNotificationProtocolEntity
from yowsup.structs import ProtocolTreeNode
class CreateGroupsNotificationProtocolEntity(GroupsNotificationProtocolEntity):
    '''
<notification notify="WhatsApp" id="{{id}}" t="1420402514" participant="{{participant_jiid}}" from="{{group_jid}}" type="w:gp2">
<create type="new">
<group subject="{{GROUPSUBJ}}" creation="{{GROUP_CREATION_TYIME}}" creator="{{CREATOR_JID}}"
    s_t="{{SUBJECT_SET_TIMESTAMP}}" id="{{GROUP_ID}}" s_o="{{SUBJECT_OWNER_JID}}">
<participant type="admin" jid="{{JID_1}}">
</participant>
<participant jid="{{JID_2}}">
</participant>
</group>
</create>
</notification>
    '''
    TYPE_CREATE_NEW = "new"
    TYPE_PARTICIPANT_ADMIN = "admin"
    def __init__(self, _id, _from, timestamp, notify, participant, offline,
                 createType, groupId, creationTimestamp, creatorJid,
                 subject, subjectTime, subjectOwnerJid,
                 participants):
        super(CreateGroupsNotificationProtocolEntity, self).__init__(_id, _from, timestamp, notify, participant, offline)
        self.setGroupProps(createType, groupId, creationTimestamp, creatorJid,
                           subject, subjectTime, subjectOwnerJid, participants)

    def setGroupProps(self, createType, groupId, creationTimestamp, creatorJid,
                      subject, subjectTime, subjectOwnerJid,
                      participants):

        assert type(participants) is dict, "Participants must be a dict {jid => type?}"

        self.createType = createType
        self.groupId = groupId
        self.creationTimestamp = int(creationTimestamp)
        self.creatorJid = creatorJid
        self.subject = subject
        self.subjectTime = int(subjectTime)
        self.subjectOwnerJid = subjectOwnerJid
        self.participants = participants

    def getParticipants(self):
        return self.participants

    def getSubject(self):
        return self.subject

    def getGroupId(self):
        return self.groupId

    def getCreationTimestamp(self):
        return self.creationTimestamp

    def getCreatorJid(self, full = True):
        return self.creatorJid if full else self.creatorJid.split('@')[0]

    def getSubjectTimestamp(self):
        return self.subjectTime

    def getSubjectOwnerJid(self, full = True):
        return self.subjectOwnerJid if full else self.subjectOwnerJid.split('@')[0]

    def getCreatetype(self):
        return self.createType

    def getGroupAdmin(self, full = True):
        for jid, _type in self.participants.items():
            if _type == self.__class__.TYPE_PARTICIPANT_ADMIN:
                return jid if full else jid.split('@')[0]

    def __str__(self):
        out = super(CreateGroupsNotificationProtocolEntity, self).__str__()
        out += "Creator: %s\n" % self.getCreatorJid()
        out += "Create type: %s\n" % self.getCreatetype()
        out += "Creation timestamp: %s\n" % self.getCreationTimestamp()
        out += "Subject: %s\n" % self.getSubject()
        out += "Subject owner: %s\n" % self.getSubjectOwnerJid()
        out += "Subject timestamp: %s\n" % self.getSubjectTimestamp()
        out += "Participants: %s\n" % self.getParticipants()
        return out

    def toProtocolTreeNode(self):
        node = super(CreateGroupsNotificationProtocolEntity, self).toProtocolTreeNode()
        createNode = ProtocolTreeNode("create", {"type": self.getCreatetype()})
        groupNode = ProtocolTreeNode("group", {
            "subject": self.getSubject(),
            "creation": str(self.getCreationTimestamp()),
            "creator": self.getCreatorJid(),
            "s_t": self.getSubjectTimestamp(),
            "s_o": self.getSubjectOwnerJid(),
            "id": self.getGroupId()
        })

        participants = []
        for jid, _type in self.getParticipants().items():
            pnode = ProtocolTreeNode("participant", {"jid": jid})
            if _type:
                pnode["type"] = _type
            participants.append(pnode)

        groupNode.addChildren(participants)
        createNode.addChild(groupNode)
        node.addChild(createNode)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        createNode = node.getChild("create")
        groupNode = createNode.getChild("group")
        participants = {}
        for p in groupNode.getAllChildren("participant"):
            participants[p["jid"]] = p["type"]

        return CreateGroupsNotificationProtocolEntity(
            node["id"], node["from"], node["t"], node["notify"], node["participant"], node["offline"],
            createNode["type"], groupNode["id"], groupNode["creation"], groupNode["creator"], groupNode["subject"],
            groupNode["s_t"], groupNode["s_o"], participants
        )
