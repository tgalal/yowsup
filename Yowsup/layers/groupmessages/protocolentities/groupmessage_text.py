from Yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .groupmessage import GroupMessageProtocolEntity
class TextGroupMessageProtocolEntity(GroupMessageProtocolEntity):
    '''
    <message participant="{{PARTICIPANT_JID}}" 
        t="{{TIME_STAMP}}" from="{{GROUP_JID}}" 
        offline="{{OFFLINE}}" type="text" id="{{MESSAGE_ID}}" notify="{{NOTIFY_NAME}}">
        <body>
            {{MESSAGE_DATA}}
        </body>
    </message>
    '''
    def __init__(self, _id, _from, participant, timestamp, notify, body, offline = False, retry = None):
        super(TextGroupMessageProtocolEntity, self).__init__("text", _id, _from, participant, timestamp, notify, offline, retry)
        self.setBody(body)

    def __str__(self):
        out  = super(TextGroupMessageProtocolEntity, self).__str__()
        out += "body: %s\n" % self.body
        return out

    def setBody(self, body):
        self.body = body

    def toProtocolTreeNode(self):
        node = super(TextGroupMessageProtocolEntity, self).toProtocolTreeNode()
        bodyNode = ProtocolTreeNode("body", {}, None, self.body)
        node.addChild(bodyNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = GroupMessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = TextGroupMessageProtocolEntity
        entity.setBody(node.getChild("body").getData())
        return entity
