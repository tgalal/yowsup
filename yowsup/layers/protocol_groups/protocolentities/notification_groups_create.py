from .notification_groups import GroupsNotificationProtocolEntity
from yowsup.structs import ProtocolTreeNode


class CreateGroupsNotificationProtocolEntity(GroupsNotificationProtocolEntity):
    """
    <notification from="{{owner_username}}-{{group_id}}@g.us" type="w:gp2" id="{{message_id}}" participant="{{participant_jid}}"
            t="{{timestamp}}" notify="{{pushname}}">
        <create type="new" key="{{owner_username}}-{{key}}@temp">
            <group id="{{group_id}}" creator="{{creator_jid}}" creation="{{creation_timestamp}}"
                    subject="{{group_subject}}" s_t="{{subject_timestamp}}" s_o="{{subject_owner_jid}}">
                <participant jid="{{pariticpant_jid}}"/>
                <participant jid="{{}}" type="superadmin"/>
            </group>
        </create>
    </notification>
    """

    TYPE_CREATE_NEW = "new"
    TYPE_PARTICIPANT_ADMIN = "admin"
    TYPE_PARTICIPANT_SUPERADMIN = "superadmin"

    def __init__(self, _id, _from, timestamp, notify, participant, offline,
                 createType, key, groupId, creationTimestamp, creatorJid,
                 subject, subjectTime, subjectOwnerJid,
                 participants):
        super(CreateGroupsNotificationProtocolEntity, self).__init__(_id, _from, timestamp, notify, participant, offline)
        self.setGroupProps(createType, key, groupId, creationTimestamp, creatorJid,
                           subject, subjectTime, subjectOwnerJid, participants)

    def setGroupProps(self, createType, key, groupId, creationTimestamp, creatorJid,
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
        self._key = key

    @property
    def key(self):
        return self._key

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

    def getGroupSuperAdmin(self, full = True):
        for jid, _type in self.participants.items():
            if _type == self.__class__.TYPE_PARTICIPANT_SUPERADMIN:
                return jid if full else jid.split('@')[0]

    def getGroupAdmins(self, full = True):
        out = []
        for jid, _type in self.participants.items():
            if _type == self.__class__.TYPE_PARTICIPANT_ADMIN:
                out.append(jid if full else jid.split('@')[0])
        return out

    def __str__(self):
        out = super(CreateGroupsNotificationProtocolEntity, self).__str__()
        out += "Creator: %s\n" % self.getCreatorJid()
        out += "Create type: %s\n" % self.getCreatetype()
        out += "Creation timestamp: %s\n" % self.getCreationTimestamp()
        out += "Subject: %s\n" % self.getSubject()
        out += "Subject owner: %s\n" % self.getSubjectOwnerJid()
        out += "Subject timestamp: %s\n" % self.getSubjectTimestamp()
        out += "Participants: %s\n" % self.getParticipants()
        out += "Key: %s\n" % self.key
        return out

    def toProtocolTreeNode(self):
        node = super(CreateGroupsNotificationProtocolEntity, self).toProtocolTreeNode()
        createNode = ProtocolTreeNode("create", {"type": self.getCreatetype(), "key": self.key})
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
            createNode["type"], createNode["key"], groupNode["id"], groupNode["creation"], groupNode["creator"], groupNode["subject"],
            groupNode["s_t"], groupNode["s_o"], participants
        )
