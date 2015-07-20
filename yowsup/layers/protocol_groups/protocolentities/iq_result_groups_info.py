from yowsup.structs import ProtocolTreeNode
from yowsup.layers.protocol_iq.protocolentities import ResultIqProtocolEntity
class InfoGroupsResultIqProtocolEntity(ResultIqProtocolEntity):
    '''
<iq type="result" from="{{GROUP_ID}}" id="{{IQ_ID}}">
  <group subject="{{GROUPSUBJ}}" creation="{{GROUP_CREATION_TYIME}}"
      creator="{{CREATOR_JID}}" s_t="{{SUBJECT_SET_TIMESTAMP}}" id="{{GROUP_ID}}"
      s_o="{{SUBJECT_OWNER_JID}}">
    <participant jid="{{PARTICIPANT_JID}}" type="admin"></participant>
    <participant jid="{{PARTICIPANT_JID}}"></participant>
    <participant jid="{{PARTICIPANT_JID}}"></participant>
  </group>
</iq>
    '''
    TYPE_PARTICIPANT_ADMIN = "admin"
    def __init__(self, _id, _from,
                 groupId, creationTimestamp, creatorJid,
                 subject, subjectTime, subjectOwnerJid,
                 participants):
        super(InfoGroupsResultIqProtocolEntity, self).__init__(_id = _id, _from = _from)
        self.setGroupProps(groupId, creationTimestamp, creatorJid,
                           subject, subjectTime, subjectOwnerJid, participants)

    def setGroupProps(self, groupId, creationTimestamp, creatorJid,
                      subject, subjectTime, subjectOwnerJid,
                      participants):

        assert type(participants) is dict, "Participants must be a dict {jid => type?}"

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

    def getGroupAdmins(self, full = True):
        admins = []
        for jid, _type in self.participants.items():
            if _type == self.__class__.TYPE_PARTICIPANT_ADMIN:
                admins.append(jid if full else jid.split('@')[0])
        return admins

    def __str__(self):
        out = super(InfoGroupsResultIqProtocolEntity, self).__str__()
        out += "Group ID: %s\n" % self.groupId
        out += "Created: %s\n" % self.creationTimestamp
        out += "Creator JID: %s\n" % self.creatorJid
        out += "Subject: %s\n" % self.subject
        out += "Subject Timestamp: %s\n" % self.subjectTime
        out += "Subject owner JID: %s\n" % self.subjectOwnerJid
        out += "Participants: %s\n" % self.participants
        return out

    def toProtocolTreeNode(self):
        node = super(InfoGroupsResultIqProtocolEntity, self).toProtocolTreeNode()
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
        node.addChild(groupNode)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        groupNode = node.getChild("group")
        participants = {}
        for p in groupNode.getAllChildren("participant"):
            participants[p["jid"]] = p["type"]

        return InfoGroupsResultIqProtocolEntity(
            node["id"], node["from"],
            groupNode["id"], groupNode["creation"], groupNode["creator"], groupNode["subject"],
            groupNode["s_t"], groupNode["s_o"], participants
        )
