from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .notification import NotificationProtocolEntity
class StatusNotificationProtocolEntity(NotificationProtocolEntity):
    '''
    <notification offline="0" id="{{NOTIFICATION_ID}}" notify="{{NOTIFY_NAME}}" type="status" 
            t="{{TIMESTAMP}}" from="{{SENDER_JID}}">
        <set>
            {{STATUS}}
        </set>
    </notification>
    
    '''

    def __init__(self, _type, _id,  _from, status, timestamp, notify, offline = False):
        super(StatusNotificationProtocolEntity, self).__init__("status", _id, _from, timestamp, notify, offline)
        self.setStatus(status)

    def setStatus(self, status):
        self.status = status
    
    def toProtocolTreeNode(self):
        node = super(StatusNotificationProtocolEntity, self).toProtocolTreeNode()
        setNode = ProtocolTreeNode("set", {}, None, self.status)
        node.addChild(setNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = NotificationProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = StatusNotificationProtocolEntity
        entity.setStatus(node.getChild("set").getData())
        return entity