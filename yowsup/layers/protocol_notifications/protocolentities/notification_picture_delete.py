from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .notification_picture import PictureNotificationProtocolEntity
class DeletePictureNotificationProtocolEntity(PictureNotificationProtocolEntity):
    '''
    <notification offline="0" id="{{NOTIFICATION_ID}}" notify="{{NOTIFY_NAME}}" type="picture" 
            t="{{TIMESTAMP}}" from="{{SENDER_JID}}">
        <delete jid="{{DELETE_JID}}">
        </delete>
    </notification>
    '''

    def __init__(self, _id,  _from, status, timestamp, notify, offline, deleteJid):
        super(DeletePictureNotificationProtocolEntity, self).__init__(_id, _from, timestamp, notify, offline)
        self.setData(deleteJid)

    def setData(self, deleteJid):
        self.deleteJid =   deleteJid

    def __str__(self):
        out = super(DeletePictureNotificationProtocolEntity, self).__str__()
        out += "Type: Delete"
        return out
    
    def toProtocolTreeNode(self):
        node = super(DeletePictureNotificationProtocolEntity, self).toProtocolTreeNode()
        deleteNode = ProtocolTreeNode("delete", {"jid": self.deleteJid}, None, None)
        node.addChild(deleteNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = PictureNotificationProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = DeletePictureNotificationProtocolEntity
        deleteNode = node.getChild("delete")
        entity.setData(deleteNode.getAttributeValue("jid"))
        return entity
