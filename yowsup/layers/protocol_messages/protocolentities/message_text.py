from .message import MessageProtocolEntity
from yowsup.layers.protocol_messages.proto.wa_pb2 import *
class TextMessageProtocolEntity(MessageProtocolEntity):
    '''
    <message t="{{TIME_STAMP}}" from="{{CONTACT_JID}}" 
        offline="{{OFFLINE}}" type="text" id="{{MESSAGE_ID}}" notify="{{NOTIFY_NAME}}">
            <body>
                {{MESSAGE_DATA}}
            </body>
    </message>
    '''
    def __init__(self, body, _id = None,  _from = None, to = None, notify = None, 
        timestamp = None, participant = None, offline = None, retry = None):
        super(TextMessageProtocolEntity, self).__init__("text",_id, _from, to, notify, timestamp, participant, offline, retry)
        self.setBody(body)

    def __str__(self):
        out  = super(TextMessageProtocolEntity, self).__str__()
        out += "Body: %s\n" % self.body
        return out

    def setBody(self, body):
        self.body = body

    def getBody(self):
        return self.body


    def toProtocolTreeNode(self):
        from yowsup.layers.axolotl.protocolentities.dec import DecProtocolEntity

        node = super(TextMessageProtocolEntity, self).toProtocolTreeNode()
        m = Message()
        m.conversation = self.getBody()
        node.addChild(DecProtocolEntity(m.SerializeToString()).toProtocolTreeNode())

        return node

    @staticmethod
    def fromProtocolTreeNode(node):
        entity = MessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = TextMessageProtocolEntity
        entity.setBody(node.getChild("body").getData())
        return entity

    @staticmethod
    def fromDecryptedMessageProtocolTreeNode(node):
        decNode = node.getChild("dec")
        assert decNode is not None
        entity = MessageProtocolEntity.fromProtocolTreeNode(node)
        entity.__class__ = TextMessageProtocolEntity
        m = Message()
        m.ParseFromString(decNode.getData())

        entity.setBody(m.conversation)
        return entity
