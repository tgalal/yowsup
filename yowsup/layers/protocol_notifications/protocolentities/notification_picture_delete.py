from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .notification_picture import PictureNotificationProtocolEntity
class DeletePictureNotificationProtocolEntity(PictureNotificationProtocolEntity):
    '''
    <notification offline="0" id="{{NOTIFICATION_ID}}" notify="{{NOTIFY_NAME}}" type="picture" 
            t="{{TIMESTAMP}}" from="{{SENDER_JID}}">
        <delete jid="{{SET_JID}}" id="{{SET_ID}}">
        </delete>
    </notification>
    '''

    def __init__(self, _id,  _from, status, timestamp, notify, offline, delJid, delId):
        super(SetPictureNotificationProtocolEntity, self).__init__(_id, _from, timestamp, notify, offline)
        self.delData(delJid, delId)

    def delData(self, delJid, delId):
        self.delJid  =    delJid
        self.delId =   delId
    
    def toProtocolTreeNode(self):
        node = super(DeletePictureNotificationProtocolEntity, self).toProtocolTreeNode()
        delNode = ProtocolTreeNode("delete", {"jid": self.delJid, "id": self.delId}, None, None)
        node.addChild(delNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = PictureNotificationProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = DeletePictureNotificationProtocolEntity
        delNode = node.getChild("delete")
        entity.delData(delNode.getAttributeValue("jid"), delNode.getAttributeValue("id"))
        return entity