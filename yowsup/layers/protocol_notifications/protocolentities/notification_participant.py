from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from yowsup.layers.protocol_notifications.protocolentities import NotificationProtocolEntity
class ParticipantNotificationProtocolEntity(NotificationProtocolEntity):
    '''
    <notification offline="0" id="{{NOTIFICATION_ID}}" notify="{{NOTIFY_NAME}}" type="contacts"
            t="{{TIMESTAMP}}" from="{{SENDER_JID}}">
    </notification>

    '''

    def __init__(self, _type, _id,  _from, timestamp, notify, participant, remove_jid, add_jid, offline = False):
        super(ParticipantNotificationProtocolEntity, self).__init__("participant", _id, _from, timestamp, notify, offline)
        self.remove_jid = remove_jid
        self.add_jid = add_jid
        self.participant = participant

    def toProtocolTreeNode(self):
        node = super(ParticipantNotificationProtocolEntity, self).toProtocolTreeNode()
        child_attr = {
            'remove': self.remove_jid,
            'add': self.add_jid
        }
        setNode = ProtocolTreeNode("modify", child_attr)
        node.addChild(setNode)
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
            node.getChild("modify").getAttribute("remove"),
            node.getChild("modify").getAttribute("add"),
            node.getAttributeValue("offline")
        )