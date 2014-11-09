from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message import MessageProtocolEntity
class TextMessageProtocolEntity(MessageProtocolEntity):
    '''
    <message t="{{TIME_STAMP}}" from="{{CONTACT_JID}}" 
        offline="{{OFFLINE}}" type="text" id="{{MESSAGE_ID}}" notify="{{NOTIFY_NAME}}">
            <body>
                {{MESSAGE_DATA}}
            </body>
    </message>
    '''
    def __init__(self, _id, _from, timestamp, notify, body, offline, retry = None):
        super(TextMessageProtocolEntity, self).__init__("text", _id, _from, timestamp, notify, offline, retry)
        self.setBody(body)

    def setBody(self, body):
        self.body = body

    def toProtocolTreeNode(self):
        node = super(TextMessageProtocolEntity, self).toProtocolTreeNode()
        bodyNode = ProtocolTreeNode("body", {}, None, self.body)
        node.addChild(bodyNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = MessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = TextMessageProtocolEntity
        entity.setBody(node.getChild("body").getData())
        return entity
