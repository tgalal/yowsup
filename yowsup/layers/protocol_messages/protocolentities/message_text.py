from .protomessage import ProtomessageProtocolEntity
from .message import MessageMetaAttributes
from .attributes.attributes_message import MessageAttributes


class TextMessageProtocolEntity(ProtomessageProtocolEntity):
    def __init__(self, body, message_meta_attributes=None, to=None):
        # flexible attributes for temp backwards compat
        assert(bool(message_meta_attributes) ^ bool(to)), "Either set message_meta_attributes, or to, and not both"
        if to:
            message_meta_attributes = MessageMetaAttributes(recipient=to)
        super(TextMessageProtocolEntity, self).__init__("text", MessageAttributes(body), message_meta_attributes)
        self.setBody(body)

    @property
    def conversation(self):
        return self.message_attributes.conversation

    @conversation.setter
    def conversation(self, value):
        self.message_attributes.conversation = value

    def getBody(self):
        #obsolete
        return self.conversation

    def setBody(self, body):
        #obsolete
        self.conversation = body
