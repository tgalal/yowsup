from .protomessage import ProtomessageProtocolEntity
from .message import MessageAttributes
class TextMessageProtocolEntity(ProtomessageProtocolEntity):
    def __init__(self, body, messageAttributes=None, to=None):
        #flexible attributes for temp backwards compat
        assert(bool(messageAttributes) ^ bool(to)), "Either set messageAttributes, or to, and not both"
        if to:
            messageAttributes = MessageAttributes(recipient=to)
        super(TextMessageProtocolEntity, self).__init__("text", messageAttributes)
        self.setBody(body)

    @property
    def conversation(self):
        return self.proto.conversation

    @conversation.setter
    def conversation(self, value):
        self.proto.conversation = value

    def getBody(self):
        #obsolete
        return self.conversation

    def setBody(self, body):
        #obsolete
        self.conversation = body
