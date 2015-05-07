from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_notifications.protocolentities import NotificationProtocolEntity


class ParticipantNotificationProtocolEntity(NotificationProtocolEntity):
    """
    <notification from="GROUP_JID" notify="NOTIFIY_NAME" participant="PARTICIPANT_JID" id="NOTIFICATION_ID" t="TIMESTAMP" type="w:gp2">
    <add>
        <participant jid="PARTICIPANT_1_JID"></participant>
        <participant jid="PARTICIPANT_2_JID"></participant>
    </add>

    <remove>
        <participant jid="PARTICIPANT_3_JID"></participant>
        <participant jid="PARTICIPANT_4_JID"></participant>
    </remove>
    </notification>
    """

    def __init__(self, _type, _id, _from, timestamp, notify, participant, remove_jid_list, add_jid_list, offline=False):
        super(ParticipantNotificationProtocolEntity, self).__init__("w:gp2", _id, _from, timestamp, notify, offline)
        self.remove_jid_list = remove_jid_list
        self.add_jid_list = add_jid_list
        self.participant = participant

    def toProtocolTreeNode(self):
        node = super(ParticipantNotificationProtocolEntity, self).toProtocolTreeNode()

        remove_node = ProtocolTreeNode("remove")
        add_node = ProtocolTreeNode("add")
        remove_node.addChildren(self.remove_jid_list)
        add_node.addChildren(self.add_jid_list)
        node.addChild(remove_node)
        node.addChild(add_node)

        node.setAttribute("participant", self.participant)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):

        return ParticipantNotificationProtocolEntity(
            node.getAttributeValue("type"),
            node.getAttributeValue("id"),
            node.getAttributeValue("from"),
            node.getAttributeValue("t"),
            node.getAttributeValue("notify"),
            node.getAttributeValue("participant"),
            node.getChild("remove").getAllChildren("participant"),
            node.getChild("add").getAllChildren("participant"),
            node.getAttributeValue("offline")
        )