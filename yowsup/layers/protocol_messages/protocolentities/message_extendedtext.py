from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message_meta import MessageMetaAttributes
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_extendedtext import ExtendedTextAttributes
from yowsup.layers.protocol_messages.protocolentities.protomessage import ProtomessageProtocolEntity
from yowsup.layers.protocol_messages.protocolentities.attributes.attributes_message import MessageAttributes


class ExtendedTextMessageProtocolEntity(ProtomessageProtocolEntity):
    def __init__(self, extended_text_attrs, message_meta_attrs):
        # type: (ExtendedTextAttributes, MessageMetaAttributes) -> None
        super(ExtendedTextMessageProtocolEntity, self).__init__(
            "text", MessageAttributes(extended_text=extended_text_attrs), message_meta_attrs
        )

    @property
    def text(self):
        return self.message_attributes.extended_text.text

    @text.setter
    def text(self, value):
        self.message_attributes.extended_text.text = value

    @property
    def context_info(self):
        return self.message_attributes.extended_text.context_info

    @context_info.setter
    def context_info(self, value):
        self.message_attributes.extended_text.context_info = value
