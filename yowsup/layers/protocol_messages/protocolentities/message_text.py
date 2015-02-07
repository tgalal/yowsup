from yowsup.structs import ProtocolEntity, ProtocolTreeNode
from .message import MessageProtocolEntity
class TextMessageProtocolEntity(MessageProtocolEntity):
    schema = (__file__, "schemas/message_text.xsd")
    '''
    <message t="{{TIME_STAMP}}" from="{{CONTACT_JID}}" 
        offline="{{OFFLINE}}" type="text" id="{{MESSAGE_ID}}" notify="{{NOTIFY_NAME}}">
            <body>
                {{MESSAGE_DATA}}
            </body>
    </message>
    '''
    def __init__(self, body, _id = None,  _from = None, to = None, notify = None, 
        timestamp = None, participant = None, offline = None, retry = None, phash = None):
        super(TextMessageProtocolEntity, self).__init__("text",_id, _from, to, notify, timestamp, participant, offline, retry, phash)
        self.setBody(body)

    def __str__(self):
        out  = super(TextMessageProtocolEntity, self).__str__()
        out += "body: %s\n" % self.body
        return out

    def setBody(self, body):
        self.body = body

    def getBody(self):
        return self.body

    def toProtocolTreeNode(self):
        node = super(TextMessageProtocolEntity, self).toProtocolTreeNode()
        bodyNode = ProtocolTreeNode("body", {}, None, self.body)
        node.addChild(bodyNode)
        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = TextMessageProtocolEntity(node.getChild("body").getData(),
                                           node["id"], node["from"], node["to"],
                                           node["notify"], node["t"], node["participant"],
                                           node["offline"], node["retry"], node["phash"])
        return entity
