from .notification_groups import GroupsNotificationProtocolEntity
from yowsup.structs import ProtocolTreeNode
class AddGroupsNotificationProtocolEntity(GroupsNotificationProtocolEntity):
    '''
<notification participant="{{participant_jiid}}" t="{{TIMESTAMP}}" from="{{group_jid}}" type="w:gp2" id="{{id}}" notify="WhatsApp">
<add>
<participant jid="{{JID_1}}">
</participant>
</add>
</notification>
    '''
    def __init__(self, _id, _from, timestamp, notify, participant, offline, participants):
        super(AddGroupsNotificationProtocolEntity, self).__init__(_id, _from, timestamp, notify, participant, offline)
        self.setParticipants(participants)

    def setParticipants(self, participants):
        assert type(participants) is list, "Must be a list of jids, got %s instead." % type(participants)
        self.participants = participants

    def getParticipants(self):
        return self.participants

    def __str__(self):
        out = super(AddGroupsNotificationProtocolEntity, self).__str__()
        out += "Participants: %s\n" % " ".join(self.getParticipants())
        return out

    def toProtocolTreeNode(self):
        node = super(AddGroupsNotificationProtocolEntity, self).toProtocolTreeNode()
        addNode = ProtocolTreeNode("add")
        participants = []
        for jid in self.getParticipants():
            pnode = ProtocolTreeNode("participant", {"jid": jid})
            participants.append(pnode)

        addNode.addChildren(participants)
        node.addChild(addNode)

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        addNode = node.getChild("add")
        participants = []
        for p in addNode.getAllChildren("participant"):
            participants.append(p["jid"])

        return AddGroupsNotificationProtocolEntity(
            node["id"], node["from"], node["t"], node["notify"], node["participant"], node["offline"],
            participants
        )