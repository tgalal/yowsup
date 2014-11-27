from yowsup.structs import ProtocolTreeNode
from .notification_contact import ContactNotificationProtocolEntity
class AddContactNotificationProtocolEntity(ContactNotificationProtocolEntity):
    '''
    <notification offline="0" id="{{NOTIFICATION_ID}}" notify="{{NOTIFY_NAME}}" type="contacts" 
            t="{{TIMESTAMP}}" from="{{SENDER_JID}}">
        <add jid="{{SET_JID}}"> </add>
    </notification>
    '''

    def __init__(self, _id,  _from, status, timestamp, notify, offline, contactJid):
        super(AddContactNotificationProtocolEntity, self).__init__(_id, _from, timestamp, notify, offline)
        self.setData(contactJid)

    def setData(self, jid):
        self.contactJid = jid

    def toProtocolTreeNode(self):
        node = super(AddContactNotificationProtocolEntity, self).toProtocolTreeNode()
        removeNode = ProtocolTreeNode("add", {"jid": self.contactJid}, None, None)
        node.addChild(removeNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = ContactNotificationProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = AddContactNotificationProtocolEntity
        removeNode = node.getChild("add")
        entity.setData(removeNode.getAttributeValue("jid"))
        return entity